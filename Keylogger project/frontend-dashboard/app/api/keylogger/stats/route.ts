import { NextResponse } from "next/server";
import { mockStats } from "@/utils/mock-data";

export async function GET() {
  return NextResponse.json({ data: mockStats });
}
