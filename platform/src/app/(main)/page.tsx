"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import FullScreenLoader from "@/components/FullScreenLoader";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    router.replace("/dashboard");
  }, [router]);

  return <FullScreenLoader />;
}
