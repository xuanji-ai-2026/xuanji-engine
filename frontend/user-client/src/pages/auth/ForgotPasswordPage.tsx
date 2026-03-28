import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { toast } from 'react-hot-toast';
import { ArrowLeft, Mail } from 'lucide-react';
import Input from '@/components/common/Input';
import Button from '@/components/common/Button';

const ForgotPasswordPage = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  const { register, handleSubmit, formState: { errors } } = useForm({
    defaultValues: { email: '' }
  });

  const onSubmit = async (data: { email: string }) => {
    setIsLoading(true);
    try {
      // API call would go here
      await new Promise(resolve => setTimeout(resolve, 1000));
      setIsSuccess(true);
      toast.success('重置链接已发送到您的邮箱');
    } catch (error) {
      toast.error('发送失败，请重试');
    } finally {
      setIsLoading(false);
    }
  };

  if (isSuccess) {
    return (
      <div className="text-center">
        <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-green-100">
          <Mail className="h-8 w-8 text-green-600" />
        </div>
        <h3 className="mb-2 text-lg font-semibold text-gray-900">
          邮件已发送
        </h3>
        <p className="mb-6 text-sm text-gray-600">
          请检查您的邮箱，点击重置链接来设置新密码
        </p>
        <a
          href="/login"
          className="inline-flex items-center text-sm font-medium text-primary-600 hover:text-primary-700"
        >
          <ArrowLeft className="mr-1 h-4 w-4" />
          返回登录
        </a>
      </div>
    );
  }

  return (
    <div>
      <h2 className="mb-2 text-center text-2xl font-bold text-gray-900">
        忘记密码
      </h2>
      <p className="mb-6 text-center text-sm text-gray-600">
        输入您的邮箱地址，我们将发送重置链接
      </p>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <Input
          label="邮箱地址"
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

        <Button
          type="submit"
          fullWidth
          isLoading={isLoading}
          className="mt-6"
        >
          发送重置链接
        </Button>

        <div className="mt-6 text-center">
          <a
            href="/login"
            className="inline-flex items-center text-sm font-medium text-primary-600 hover:text-primary-700"
          >
            <ArrowLeft className="mr-1 h-4 w-4" />
            返回登录
          </a>
        </div>
      </form>
    </div>
  );
};

export default ForgotPasswordPage;
