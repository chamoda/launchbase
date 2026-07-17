export default function FullScreenLoader() {
  return (
    <div className="flex h-screen items-center justify-center">
      <svg
        viewBox="0 0 64 64"
        className="size-16 text-foreground"
        role="img"
        aria-label="Loading"
      >
        {/* dome lifts off above the pad, then loops */}
        <path
          className="launch-loader__dome"
          d="M12 35 A20 20 0 0 1 52 35 Z"
          fill="currentColor"
        />
        {/* launchpad bar pulses like exhaust */}
        <rect
          className="launch-loader__pad"
          x="12"
          y="43"
          width="40"
          height="7"
          rx="3.5"
          fill="#FF4F1F"
        />
      </svg>
    </div>
  );
}
