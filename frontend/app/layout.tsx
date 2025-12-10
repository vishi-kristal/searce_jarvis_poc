import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Kristal Agent PoC",
  description: "Proof of Concept UI for Kristal Agent",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}

