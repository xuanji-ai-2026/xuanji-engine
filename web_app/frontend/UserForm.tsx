/**
 * 前端 - 管理后台 - 用户管理 - 用户表单组件
 * 任务ID: TASK-0012
 */

import React, { useState } from 'react';

interface UserFormProps {
  onSubmit: (data: UserData) => void;
}

interface UserData {
  username: string;
  email: string;
  password: string;
}

export const UserForm: React.FC<UserFormProps> = ({ onSubmit }) => {
  const [formData, setFormData] = useState<UserData>({
    username: '',
    email: '',
    password: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="username">用户名</label>
        <input
          type="text"
          id="username"
          value={formData.username}
          onChange={(e) => setFormData({ ...formData, username: e.target.value })}
          className="mt-1 block w-full"
        />
      </div>
      <div>
        <label htmlFor="email">邮箱</label>
        <input
          type="email"
          id="email"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          className="mt-1 block w-full"
        />
      </div>
      <div>
        <label htmlFor="password">密码</label>
        <input
          type="password"
          id="password"
          value={formData.password}
          onChange={(e) => setFormData({ ...formData, password: e.target.value })}
          className="mt-1 block w-full"
        />
      </div>
      <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">
        提交
      </button>
    </form>
  );
};
