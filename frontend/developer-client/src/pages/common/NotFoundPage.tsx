import React from 'react';
import { Link } from 'react-router-dom';
import { Home, ArrowLeft } from 'lucide-react';
import { Button } from '../../components/Button';
import { Card, CardContent } from '../../components/Card';

export const NotFoundPage: React.FC = () => {
  return (
    <div className="min-h-[60vh] flex items-center justify-center">
      <Card className="max-w-md w-full">
        <CardContent className="pt-12 pb-12 text-center">
          <div className="text-6xl font-bold text-primary mb-4">404</div>
          <h2 className="text-2xl font-bold mb-2">页面未找到</h2>
          <p className="text-muted-foreground mb-8">
            抱歉，您访问的页面不存在
          </p>
          <div className="flex gap-3 justify-center">
            <Button variant="outline" icon={<ArrowLeft className="h-4 w-4" />}>
              返回
            </Button>
            <Link to="/">
              <Button icon={<Home className="h-4 w-4" />}>
                首页
              </Button>
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
