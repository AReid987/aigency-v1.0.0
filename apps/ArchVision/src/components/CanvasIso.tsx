const CanvasIso = () => {
  return (
    <div className="w-full h-full bg-white">
      <svg
        viewBox="0 0 800 600"
        className="w-full h-full"
        style={{ transform: 'rotate(45deg)' }}
      >
        <g transform="skew(-30)">
          <rect
            x="300"
            y="250"
            width="100"
            height="100"
            fill="#e2e8f0"
            stroke="#64748b"
            strokeWidth="2"
          />
        </g>
      </svg>
    </div>
  );
};

export default CanvasIso;