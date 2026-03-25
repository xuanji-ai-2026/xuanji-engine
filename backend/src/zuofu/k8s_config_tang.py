"""
K8s Config Module
Author: 汤左膀 (Employee ID: 147)
Group: XJ-07 左辅星
Task: K8s配置实现
"""

from typing import Dict, List, Any, Optional
import yaml


class K8sConfig:
    """K8s Configuration Implementation"""
    
    def __init__(self):
        """Initialize the K8s config module."""
        self.configs: Dict[str, Dict] = {}
        
    def create_deployment(self, name: str, image: str, replicas: int = 1) -> Dict:
        """
        Create a Kubernetes deployment config.
        
        Args:
            name: Deployment name
            image: Container image
            replicas: Number of replicas
            
        Returns:
            Deployment config
        """
        config = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": name
            },
            "spec": {
                "replicas": replicas,
                "selector": {
                    "matchLabels": {
                        "app": name
                    }
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": name
                        }
                    },
                    "spec": {
                        "containers": [{
                            "name": name,
                            "image": image,
                            "ports": [{
                                "containerPort": 80
                            }]
                        }]
                    }
                }
            }
        }
        
        self.configs[f"deployment-{name}"] = config
        return config
        
    def create_service(self, name: str, service_type: str = "ClusterIP") -> Dict:
        """
        Create a Kubernetes service config.
        
        Args:
            name: Service name
            service_type: Service type
            
        Returns:
            Service config
        """
        config = {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "name": name
            },
            "spec": {
                "selector": {
                    "app": name
                },
                "ports": [{
                    "port": 80,
                    "targetPort": 80
                }],
                "type": service_type
            }
        }
        
        self.configs[f"service-{name}"] = config
        return config
        
    def create_configmap(self, name: str, data: Dict[str, str]) -> Dict:
        """Create a ConfigMap."""
        config = {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {
                "name": name
            },
            "data": data
        }
        
        self.configs[f"configmap-{name}"] = config
        return config
        
    def export_yaml(self, config_name: str) -> str:
        """Export config as YAML."""
        if config_name in self.configs:
            return yaml.dump(self.configs[config_name])
        return ""
        
    def get_status(self) -> Dict[str, Any]:
        """Get module status."""
        return {
            "configs_count": len(self.configs)
        }
        
    def get_result(self) -> Dict[str, Any]:
        """Get module result."""
        return {
            "module": "K8sConfig",
            "version": "1.0.0",
            "status": "ready"
        }
