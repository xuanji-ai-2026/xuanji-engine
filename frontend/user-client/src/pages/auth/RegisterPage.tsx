import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { toast } from 'react-hot-toast';
import { useAuthStore } from '@/stores';
import Input from '@/components/common/Input';
import Button from '@/components/common/Button';
import type { RegisterRequest } from '@/types';

const RegisterPage = () => {
  const navigate = useNavigate();
  const registerUser = useAuthStore((state) => state.register);
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<RegisterRequest>();

  const password = watch('password');

  const onSubmit = async (data: RegisterRequest) => {
    setIsLoading(true);
    try {
      await registerUser(data);
      toast.success('注册成功');
      navigate('/dashboard');
    } catch (error) {
      toast.error(error instanceof Error ? error.message : '注册失败');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <h2 className="mb-6 text-center text-2xl font-bold text-gray-900">
        注册
      </h2>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <Input
          label="用户名"
          placeholder="4-20位字母、数字、下划线"
          error={errors.username?.message}
          {...register('username', {
            required: '请输入用户名',
            minLength: { value: 4, message: '用户名至少4位' },
            maxLength: { value: 20, message: '用户名最多20位' },
            pattern: {
              value: /^[a-zA-Z0-9_]+$/,
              message: '只能包含字母、数字、下划线',
            },
          })}
        />

        <Input
          label="邮箱"
          type="email"
          placeholder="请输入邮箱"
          error={errors.email?.message}
          {...register('email', {
            required: '请输入邮箱',
            pattern: {
              value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
              message: '请输入有效的邮箱地址',
            },
          })}
        />

        <Input
          label="密码"
          type="password"
          placeholder="至少8位"
          error={errors.password?.message}
          {...register('password', {
            required: '请输入密码',
            minLength: { value: 8, message: '密码至少8位' },
          })}
        />

        <Input
          label="确认密码"
          type="password"
          placeholder="再次输入密码"
          error={errors.confirmPassword?.message}
          {...register('confirmPassword', {
            required: '请确认密码',
            validate: (value) => value === password || '两次密码不一致',
          })}
        />

        <Button
          type="submit"
          fullWidth
          isLoading={isLoading}
          className="mt-6"
        >
          注册
        </Button>

        <div className="mt-6 text-center text-sm">
          <span className="text-gray-600">已有账号? </span>
          <a
            href="/login"
            className="font-medium text-primary-600 hover:text-primary-700"
          >
            立即登录
          </a>
        </div>
      </form>
    </div>
  );
};

export default RegisterPage;
