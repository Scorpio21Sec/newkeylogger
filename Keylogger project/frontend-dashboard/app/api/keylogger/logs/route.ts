import { NextResponse } from "next/server";
import { mockLogs } from "@/utils/mock-data";

export async function GET() {
  return NextResponse.json({ data: mockLogs });
}
