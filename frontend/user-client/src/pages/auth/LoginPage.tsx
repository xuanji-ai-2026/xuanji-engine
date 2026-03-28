import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { toast } from 'react-hot-toast';
import { useAuthStore } from '@/stores';
import Input from '@/components/common/Input';
import Button from '@/components/common/Button';
import type { LoginRequest } from '@/types';

const LoginPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const login = useAuthStore((state) => state.login);
  const [isLoading, setIsLoading] = useState(false);

  const from = (location.state as any)?.from?.pathname || '/dashboard';

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginRequest>();

  const onSubmit = async (data: LoginRequest) => {
    setIsLoading(true);
    try {
      await login(data.username, data.password);
      toast.success('登录成功');
      navigate(from, { replace: true });
    } catch (error) {
      toast.error(error instanceof Error ? error.message : '登录失败');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <h2 className="mb-6 text-center text-2xl font-bold text-gray-900">
        登录
      </h2>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <Input
          label="用户名"
          placeholder="请输入用户名"
          error={errors.username?.message}
          {...register('username', {
            required: '请输入用户名',
            minLength: { value: 4, message: '用户名至少4位' },
          })}
        />

        <Input
          label="密码"
          type="password"
          placeholder="请输入密码"
          error={errors.password?.message}
          {...register('password', {
            required: '请输入密码',
            minLength: { value: 6, message: '密码至少6位' },
          })}
        />

        <div className="flex items-center justify-between">
          <label className="flex items-center">
            <input
              type="checkbox"
              className="h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
            />
            <span className="ml-2 text-sm text-gray-600">记住我</span>
          </label>
          <a
            href="/forgot-password"
            className="text-sm text-primary-600 hover:text-primary-700"
          >
            忘记密码?
          </a>
        </div>

        <Button
          type="submit"
          fullWidth
          isLoading={isLoading}
          className="mt-6"
        >
          登录
        </Button>

        <div className="mt-6 text-center text-sm">
          <span className="text-gray-600">还没有账号? </span>
          <a
            href="/register"
            className="font-medium text-primary-600 hover:text-primary-700"
          >
            立即注册
          </a>
        </div>
      </form>
    </div>
  );
};

export default LoginPage;
