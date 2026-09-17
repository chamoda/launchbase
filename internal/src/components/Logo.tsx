import { cn } from "@/lib/utils";

// Launchbase lockup: mark + wordmark share one coordinate system so the gap
// is exact. Canonical geometry lives in /branding. The dome and "Launch"
// inherit currentColor (theme-aware); the pad bar and "base" carry Flame.
export function Logomark({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 64 64"
      className={className}
      role="img"
      aria-label="Launchbase logomark"
    >
      <path d="M12 35 A20 20 0 0 1 52 35 Z" fill="currentColor" />
      <rect x="12" y="43" width="40" height="7" rx="3.5" fill="#FF4F1F" />
    </svg>
  );
}

export function Logo({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 340 64"
      overflow="visible"
      className={cn("h-8 w-auto", className)}
      role="img"
      aria-label="Launchbase"
    >
      <g fill="currentColor" transform="translate(-12 -3.5)">
        <path d="M12 35 A20 20 0 0 1 52 35 Z" />
        <rect x="12" y="43" width="40" height="7" rx="3.5" fill="#FF4F1F" />
      </g>
      <text
        x="57"
        y="46"
        fontFamily="Inter, 'SF Pro Display', 'Segoe UI', system-ui, sans-serif"
        fontSize="48"
        fontWeight="600"
        letterSpacing="-0.8"
        fill="currentColor"
      >
        Launch
        <tspan fill="#FF4F1F">base</tspan>
      </text>
    </svg>
  );
}
