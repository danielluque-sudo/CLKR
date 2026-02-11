import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Colombian Legal Database - Base de Datos Legal Colombiana",
  description: "Plataforma moderna para consultar, buscar y analizar leyes colombianas. Powered by AI.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
