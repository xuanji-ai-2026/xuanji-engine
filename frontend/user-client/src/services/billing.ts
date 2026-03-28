import apiService from './api';
import type {
  Account,
  Transaction,
  Bill,
  Invoice,
  RechargeRequest,
  PaymentMethod,
  Subscription,
  Plan,
  PaginationRequest,
  PaginationResponse,
} from '@/types';

class BillingService {
  // 账户管理

  // 获取账户信息
  async getAccount(): Promise<Account> {
    const response = await apiService.get<Account>('/billing/account');
    return response.data as Account;
  }

  // 获取交易记录
  async getTransactions(
    params: PaginationRequest
  ): Promise<PaginationResponse<Transaction>> {
    const response = await apiService.get<PaginationResponse<Transaction>>(
      '/billing/transactions',
      { params }
    );
    return response.data as PaginationResponse<Transaction>;
  }

  // 充值
  async recharge(data: RechargeRequest): Promise<{
    paymentUrl: string;
    transactionId: string;
  }> {
    const response = await apiService.post('/billing/recharge', data);
    return response.data as {
      paymentUrl: string;
      transactionId: string;
    };
  }

  // 获取支付方式列表
  async getPaymentMethods(): Promise<PaymentMethod[]> {
    const response = await apiService.get<PaymentMethod[]>('/billing/payment-methods');
    return response.data as PaymentMethod[];
  }

  // 账单管理

  // 获取账单列表
  async getBills(params: PaginationRequest): Promise<PaginationResponse<Bill>> {
    const response = await apiService.get<PaginationResponse<Bill>>(
      '/billing/bills',
      { params }
    );
    return response.data as PaginationResponse<Bill>;
  }

  // 获取单个账单
  async getBill(id: string): Promise<Bill> {
    const response = await apiService.get<Bill>(`/billing/bills/${id}`);
    return response.data as Bill;
  }

  // 支付账单
  async payBill(id: string, paymentMethod: string): Promise<{
    paymentUrl: string;
    transactionId: string;
  }> {
    const response = await apiService.post(`/billing/bills/${id}/pay`, {
      paymentMethod,
    });
    return response.data as {
      paymentUrl: string;
      transactionId: string;
    };
  }

  // 发票管理

  // 获取发票列表
  async getInvoices(params: PaginationRequest): Promise<PaginationResponse<Invoice>> {
    const response = await apiService.get<PaginationResponse<Invoice>>(
      '/billing/invoices',
      { params }
    );
    return response.data as PaginationResponse<Invoice>;
  }

  // 申请发票
  async requestInvoice(
    billId: string,
    data: {
      type: 'electronic' | 'paper';
      title: string;
      taxId: string;
      email?: string;
      address?: string;
    }
  ): Promise<Invoice> {
    const response = await apiService.post<Invoice>('/billing/invoices', {
      billId,
      ...data,
    });
    return response.data as Invoice;
  }

  // 套餐管理

  // 获取套餐列表
  async getPlans(): Promise<Plan[]> {
    const response = await apiService.get<Plan[]>('/billing/plans');
    return response.data as Plan[];
  }

  // 获取当前订阅
  async getCurrentSubscription(): Promise<Subscription> {
    const response = await apiService.get<Subscription>('/billing/subscription');
    return response.data as Subscription;
  }

  // 订阅套餐
  async subscribe(planId: string, period: 'monthly' | 'yearly'): Promise<{
    paymentUrl: string;
    subscriptionId: string;
  }> {
    const response = await apiService.post('/billing/subscription', {
      planId,
      period,
    });
    return response.data as {
      paymentUrl: string;
      subscriptionId: string;
    };
  }

  // 取消订阅
  async cancelSubscription(): Promise<void> {
    await apiService.post('/billing/subscription/cancel');
  }

  // 恢复订阅
  async resumeSubscription(): Promise<void> {
    await apiService.post('/billing/subscription/resume');
  }

  // 查询订单状态
  async getTransactionStatus(transactionId: string): Promise<{
    status: 'pending' | 'completed' | 'failed' | 'cancelled';
  }> {
    const response = await apiService.get(`/billing/transactions/${transactionId}/status`);
    return response.data as {
      status: 'pending' | 'completed' | 'failed' | 'cancelled';
    };
  }
}

export const billingService = new BillingService();
export default billingService;
