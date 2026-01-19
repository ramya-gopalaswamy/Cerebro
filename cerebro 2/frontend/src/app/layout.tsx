import type { Metadata } from 'next';
import '../styles/globals.css';
import '../styles/animations.css';
import ChatbotClient from './ChatbotClient';

export const metadata: Metadata = {
  title: 'Cerebro - Workflow Accountability',
  description: 'Track daily goals and build accountability for job seekers',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="corememories-bg">
        {children}
        <ChatbotClient />
      </body>
    </html>
  );
}
