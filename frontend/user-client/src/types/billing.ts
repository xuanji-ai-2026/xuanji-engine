// 计费相关类型
export interface Account {
  id: string;
  userId: string;
  balance: number;
  currency: string;
  frozenAmount: number;
  creditLimit: number;
  status: 'active' | 'suspended' | 'closed';
  createdAt: string;
  updatedAt: string;
}

export interface Transaction {
  id: string;
  accountId: string;
  type: 'recharge' | 'consume' | 'refund' | 'reward' | 'withdraw';
  amount: number;
  currency: string;
  balanceBefore: number;
  balanceAfter: number;
  description: string;
  category: string;
  status: 'pending' | 'completed' | 'failed' | 'cancelled';
  metadata?: Record<string, unknown>;
  createdAt: string;
  completedAt?: string;
}

export interface Bill {
  id: string;
  accountId: string;
  billingPeriod: {
    start: string;
    end: string;
  };
  totalAmount: number;
  currency: string;
  items: BillItem[];
  status: 'unpaid' | 'paid' | 'overdue' | 'cancelled';
  dueDate: string;
  paidAt?: string;
  createdAt: string;
  updatedAt: string;
}

export interface BillItem {
  id: string;
  service: string;
  description: string;
  quantity: number;
  unitPrice: number;
  amount: number;
  category: string;
}

export interface Invoice {
  id: string;
  billId: string;
  invoiceNumber: string;
  type: 'electronic' | 'paper';
  status: 'pending' | 'issued' | 'delivered' | 'void';
  invoiceUrl?: string;
  createdAt: string;
  issuedAt?: string;
  deliveredAt?: string;
}

export interface RechargeRequest {
  amount: number;
  paymentMethod: string;
  metadata?: Record<string, unknown>;
}

export interface PaymentMethod {
  id: string;
  type: 'alipay' | 'wechat' | 'card' | 'bank';
  displayName: string;
  icon?: string;
  enabled: boolean;
  minAmount: number;
  maxAmount: number;
}

// 套餐相关
export interface Subscription {
  id: string;
  accountId: string;
  planId: string;
  planName: string;
  status: 'active' | 'trial' | 'expired' | 'cancelled';
  startDate: string;
  endDate: string;
  autoRenew: boolean;
  features: string[];
  createdAt: string;
  updatedAt: string;
}

export interface Plan {
  id: string;
  name: string;
  displayName: string;
  description: string;
  price: {
    monthly: number;
    yearly: number;
  };
  currency: string;
  features: string[];
  limits: {
    digitalHumans: number;
    chatsPerMonth: number;
    tokensPerMonth: number;
    plugins: number;
  };
  isPopular: boolean;
}
