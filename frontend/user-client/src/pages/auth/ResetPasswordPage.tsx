import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { toast } from 'react-hot-toast';
import { CheckCircle2 } from 'lucide-react';
import Input from '@/components/common/Input';
import Button from '@/components/common/Button';

const ResetPasswordPage = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  const { register, handleSubmit, watch, formState: { errors } } = useForm({
    defaultValues: { password: '', confirmPassword: '' }
  });

  const password = watch('password');

  const onSubmit = async (data: { password: string; confirmPassword: string }) => {
    setIsLoading(true);
    try {
      // API call would go here
      await new Promise(resolve => setTimeout(resolve, 1000));
      setIsSuccess(true);
      toast.success('密码重置成功');
    } catch (error) {
      toast.error('重置失败，请重试');
    } finally {
      setIsLoading(false);
    }
  };

  if (isSuccess) {
    return (
      <div className="text-center">
        <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-green-100">
          <CheckCircle2 className="h-8 w-8 text-green-600" />
        </div>
        <h3 className="mb-2 text-lg font-semibold text-gray-900">
          密码重置成功
        </h3>
        <p className="mb-6 text-sm text-gray-600">
          您的密码已成功重置，现在可以使用新密码登录
        </p>
        <Button fullWidth onClick={() => navigate('/login')}>
          返回登录
        </Button>
      </div>
    );
  }

  return (
    <div>
      <h2 className="mb-2 text-center text-2xl font-bold text-gray-900">
        设置新密码
      </h2>
      <p className="mb-6 text-center text-sm text-gray-600">
        请输入您的新密码（至少8位）
      </p>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <Input
          label="新密码"
          type="password"
          placeholder="请输入新密码"
          error={errors.password?.message}
          {...register('password', {
            required: '请输入新密码',
            minLength: { value: 8, message: '密码至少8位' },
          })}
        />

        <Input
          label="确认新密码"
          type="password"
          placeholder="再次输入新密码"
          error={errors.confirmPassword?.message}
          {...register('confirmPassword', {
            required: '请确认新密码',
            validate: (value) => value === password || '两次密码不一致',
          })}
        />

        <Button
          type="submit"
          fullWidth
          isLoading={isLoading}
          className="mt-6"
        >
          重置密码
        </Button>
      </form>
    </div>
  );
};

export default ResetPasswordPage;
