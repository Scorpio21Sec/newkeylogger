import { NextResponse } from "next/server";
import { mockSessions } from "@/utils/mock-data";

export async function GET() {
  return NextResponse.json({ data: mockSessions });
}
