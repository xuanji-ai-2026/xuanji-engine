"""
左辅星 - K8s配置模块
系统底座、容器编排、多租户
"""

import yaml
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class ContainerConfig(BaseModel):
    """容器配置"""
    name: str
    image: str
    ports: List[int] = Field(default_factory=list)
    env: Dict[str, str] = Field(default_factory=dict)
    resources: Dict[str, str] = Field(default_factory=dict)


class DeploymentConfig(BaseModel):
    """部署配置"""
    name: str
    replicas: int = Field(default=1)
    containers: List[ContainerConfig]
    service_type: str = Field(default="ClusterIP")


class K8sManifestGenerator:
    """K8s清单生成器"""
    
    def __init__(self, namespace: str = "xuanji"):
        self.namespace = namespace
    
    def generate_deployment(self, config: DeploymentConfig) -> dict:
        """生成Deployment YAML"""
        containers = []
        for c in config.containers:
            container = {
                "name": c.name,
                "image": c.image,
                "ports": [{"containerPort": p} for p in c.ports],
                "env": [{"name": k, "value": v} for k, v in c.env.items()]
            }
            if c.resources:
                container["resources"] = c.resources
            containers.append(container)
        
        return {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": config.name,
                "namespace": self.namespace
            },
            "spec": {
                "replicas": config.replicas,
                "selector": {
                    "matchLabels": {"app": config.name}
                },
                "template": {
                    "metadata": {
                        "labels": {"app": config.name}
                    },
                    "spec": {"containers": containers}
                }
            }
        }
    
    def generate_service(self, name: str, service_type: str = "ClusterIP") -> dict:
        """生成Service YAML"""
        return {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "name": f"{name}-service",
                "namespace": self.namespace
            },
            "spec": {
                "selector": {"app": name},
                "ports": [{"port": 80, "targetPort": 80}],
                "type": service_type
            }
        }
    
    def generate_ingress(self, name: str, host: str) -> dict:
        """生成Ingress YAML"""
        return {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "Ingress",
            "metadata": {
                "name": f"{name}-ingress",
                "namespace": self.namespace
            },
            "spec": {
                "rules": [{
                    "host": host,
                    "http": {
                        "paths": [{
                            "path": "/",
                            "pathType": "Prefix",
                            "backend": {
                                "service": {
                                    "name": f"{name}-service",
                                    "port": {"number": 80}
                                }
                            }
                        }]
                    }
                }]
            }
        }
    
    def generate_configmap(self, name: str, data: Dict[str, str]) -> dict:
        """生成ConfigMap"""
        return {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {
                "name": name,
                "namespace": self.namespace
            },
            "data": data
        }


class MultiTenantManager:
    """多租户管理器"""
    
    def __init__(self):
        self.tenants: Dict[str, dict] = {}
    
    def create_tenant(self, tenant_id: str, name: str, quota: dict = None) -> dict:
        """创建租户"""
        tenant = {
            "id": tenant_id,
            "name": name,
            "quota": quota or {
                "cpu": "2",
                "memory": "4Gi",
                "storage": "10Gi"
            },
            "namespaces": []
        }
        self.tenants[tenant_id] = tenant
        return tenant
    
    def create_namespace(self, tenant_id: str, namespace: str) -> bool:
        """为租户创建命名空间"""
        if tenant_id not in self.tenants:
            return False
        self.tenants[tenant_id]["namespaces"].append(namespace)
        return True
    
    def get_tenant(self, tenant_id: str) -> Optional[dict]:
        """获取租户信息"""
        return self.tenants.get(tenant_id)


class K8sDeployer(BaseModel):
    """K8s部署器 - 负责应用部署和管理"""
    
    def __init__(self, namespace: str = "xuanji"):
        self.namespace = namespace
        self.generator = K8sManifestGenerator(namespace)
        self.deployed_apps: Dict[str, Dict] = {}
    
    def deploy_application(
        self,
        name: str,
        image: str,
        replicas: int = 1,
        ports: List[int] = None,
        env: Dict[str, str] = None,
        create_service: bool = True,
        create_ingress: bool = False,
        ingress_host: str = None
    ) -> Dict:
        """部署应用"""
        # 创建Deployment配置
        deployment_config = DeploymentConfig(
            name=name,
            replicas=replicas,
            containers=[
                ContainerConfig(
                    name=name,
                    image=image,
                    ports=ports or [8080],
                    env=env or {}
                )
            ]
        )
        
        # 生成Deployment清单
        deployment_manifest = self.generator.generate_deployment(deployment_config)
        
        # 生成Service清单
        service_manifest = None
        if create_service:
            service_manifest = self.generator.generate_service(name, "ClusterIP")
        
        # 生成Ingress清单
        ingress_manifest = None
        if create_ingress and ingress_host:
            ingress_manifest = self.generator.generate_ingress(name, ingress_host)
        
        # 记录部署信息
        self.deployed_apps[name] = {
            "name": name,
            "image": image,
            "replicas": replicas,
            "namespace": self.namespace,
            "status": "deployed",
            "deployment": deployment_manifest,
            "service": service_manifest,
            "ingress": ingress_manifest,
            "deployed_at": __import__('time').time()
        }
        
        return {
            "status": "success",
            "app_name": name,
            "namespace": self.namespace,
            "replicas": replicas,
            "deployment": deployment_manifest,
            "service": service_manifest,
            "ingress": ingress_manifest
        }
    
    def scale_application(self, name: str, replicas: int) -> bool:
        """扩缩容应用"""
        if name not in self.deployed_apps:
            return False
        
        self.deployed_apps[name]["replicas"] = replicas
        
        # 更新Deployment清单
        deployment = self.deployed_apps[name]["deployment"]
        deployment["spec"]["replicas"] = replicas
        
        return True
    
    def rollback_application(self, name: str) -> bool:
        """回滚应用"""
        if name not in self.deployed_apps:
            return False
        
        # 简化实现：标记为回滚状态
        self.deployed_apps[name]["status"] = "rolling_back"
        
        return True
    
    def get_application_status(self, name: str) -> Optional[Dict]:
        """获取应用状态"""
        return self.deployed_apps.get(name)
    
    def list_applications(self) -> List[Dict]:
        """列出所有应用"""
        return list(self.deployed_apps.values())
    
    def delete_application(self, name: str) -> bool:
        """删除应用"""
        if name in self.deployed_apps:
            del self.deployed_apps[name]
            return True
        return False
    
    def update_application(
        self,
        name: str,
        image: str = None,
        replicas: int = None,
        env: Dict[str, str] = None
    ) -> bool:
        """更新应用"""
        if name not in self.deployed_apps:
            return False
        
        app = self.deployed_apps[name]
        
        if image:
            app["image"] = image
            # 更新容器镜像
            app["deployment"]["spec"]["template"]["spec"]["containers"][0]["image"] = image
        
        if replicas:
            app["replicas"] = replicas
            app["deployment"]["spec"]["replicas"] = replicas
        
        if env:
            # 更新环境变量
            for container in app["deployment"]["spec"]["template"]["spec"]["containers"]:
                if "env" not in container:
                    container["env"] = []
                # 合并环境变量
                existing = {e["name"]: e["value"] for e in container["env"]}
                existing.update(env)
                container["env"] = [{"name": k, "value": v} for k, v in existing.items()]
        
        return True
    
    def get_pod_status(self, app_name: str) -> List[Dict]:
        """获取Pod状态"""
        if app_name not in self.deployed_apps:
            return []
        
        replicas = self.deployed_apps[app_name]["replicas"]
        # 模拟Pod状态
        return [
            {
                "name": f"{app_name}-{i}",
                "status": "Running",
                "ready": True,
                "restarts": 0,
                "age": f"{i}m"
            }
            for i in range(replicas)
        ]


# 测试代码
if __name__ == "__main__":
    gen = K8sManifestGenerator()
    
    # 生成Deployment
    deployment = DeploymentConfig(
        name="xuanji-engine",
        replicas=3,
        containers=[
            ContainerConfig(
                name="api",
                image="xuanji/api:latest",
                ports=[8000],
                env={"ENV": "production"}
            )
        ]
    )
    
    manifest = gen.generate_deployment(deployment)
    print(yaml.dump(manifest, default_flow_style=False))
