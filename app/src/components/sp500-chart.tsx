"use client";

import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";
import { useTheme } from "@/lib/theme-provider";

interface ChartDataPoint {
  date: string;
  value: number;
}

interface SP500ChartProps {
  data?: ChartDataPoint[];
}

const FALLBACK_DATA: ChartDataPoint[] = [];

export function SP500Chart({ data = FALLBACK_DATA }: SP500ChartProps) {
  const { resolvedTheme } = useTheme();
  const isDark = resolvedTheme === "dark";

  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-[320px] text-foreground-subtle text-sm">
        市场数据加载中...
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={320}>
      <LineChart data={data} margin={{ top: 8, right: 16, bottom: 8, left: 0 }}>
        <CartesianGrid
          strokeDasharray="3 3"
          stroke={isDark ? "rgba(245,245,247,0.06)" : "rgba(10,10,15,0.06)"}
        />
        <XAxis
          dataKey="date"
          tick={{ fontSize: 11, fill: isDark ? "rgba(245,245,247,0.4)" : "rgba(10,10,15,0.4)" }}
          tickLine={false}
          axisLine={false}
        />
        <YAxis
          domain={["dataMin - 10", "dataMax + 10"]}
          tick={{ fontSize: 11, fill: isDark ? "rgba(245,245,247,0.4)" : "rgba(10,10,15,0.4)" }}
          tickLine={false}
          axisLine={false}
          tickFormatter={(v) => v.toLocaleString()}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: isDark ? "#1C1C1E" : "#FFFFFF",
            border: `1px solid ${isDark ? "rgba(245,245,247,0.1)" : "rgba(10,10,15,0.1)"}`,
            borderRadius: "12px",
            boxShadow: "0 4px 16px rgba(0,0,0,0.16)",
            fontSize: "13px",
          }}
          labelStyle={{ color: isDark ? "rgba(245,245,247,0.6)" : "rgba(10,10,15,0.6)" }}
          itemStyle={{ color: isDark ? "#F5F5F7" : "#0A0A0F" }}
          formatter={(value: unknown) => {
            if (typeof value === "number") return [value.toLocaleString(), "SPY"];
            return [String(value), "SPY"];
          }}
        />
        <Line
          type="monotone"
          dataKey="value"
          stroke="#007AFF"
          strokeWidth={2}
          dot={false}
          activeDot={{ r: 4, stroke: "#007AFF", strokeWidth: 2, fill: isDark ? "#0A0A0F" : "#F5F5F7" }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
