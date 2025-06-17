import React, { useState } from "react";
import ReactDOM from "react-dom/client";
import {
  CanvasProvider,
  InfiniteCanvas,
  ViewSelector,
  Toolbar,
  ViewType,
  CanvasMode,
} from "../index";

import "../styles.css";

function Demo() {
  const [mode, setMode] = useState<CanvasMode>("hybrid");
  const [view, setView] = useState<ViewType>("2d");

  return (
    <CanvasProvider
      config={{
        enableAI: true,
        enableCollaboration: true,
        enableIsometric: true,
        theme: "light",
        defaultView: "2d",
        defaultMode: "hybrid",
      }}
      data-oid="41bx8_1"
    >
      <div className="w-full h-full relative" data-oid="z5yn3db">
        <InfiniteCanvas
          mode={mode}
          defaultView={view}
          onViewChange={setView}
          onModeChange={setMode}
          data-oid="b.gt8is"
        />

        <div className="absolute top-4 left-4 z-10" data-oid="7946wqt">
          <Toolbar mode={mode} onModeChange={setMode} data-oid="wmsrqe6" />
        </div>
        <div className="absolute top-4 right-4 z-10" data-oid="5bc6i:2">
          <ViewSelector
            currentView={view}
            onViewChange={setView}
            data-oid=":qt8lnp"
          />
        </div>
      </div>
    </CanvasProvider>
  );
}

const root = document.getElementById("root");
if (root) {
  ReactDOM.createRoot(root).render(
    <React.StrictMode data-oid="tsk5qil">
      <Demo data-oid="4piqr:f" />
    </React.StrictMode>,
  );
}
