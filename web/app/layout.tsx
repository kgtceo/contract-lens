import type { Metadata } from "next";
import "./globals.css";

const url = "https://contract-lens.kareemghazal.com";
const title = "contract-lens — spot the risky clauses in a contract";
const description =
  "Paste a contract or terms-of-service and get risk-ranked clause findings (auto-renewal, liability, IP assignment, data rights…) with a verbatim quote, grounded in the document. Educational — not legal advice.";

export const metadata: Metadata = {
  metadataBase: new URL(url),
  title,
  description,
  alternates: { canonical: "/" },
  openGraph: {
    type: "website",
    url,
    siteName: "contract-lens",
    title,
    description,
    locale: "en_GB",
    images: [{ url: "/og.jpg", width: 1200, height: 630, alt: "contract-lens — AI contract / ToS reviewer" }],
  },
  twitter: { card: "summary_large_image", title, description, images: ["/og.jpg"] },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
