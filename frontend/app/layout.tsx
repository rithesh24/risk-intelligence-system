import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Risk Intelligence Dashboard",
  description: "Multi-Agent Business Risk Intelligence System",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="noise-bg min-h-screen">{children}</body>
    </html>
  );
}