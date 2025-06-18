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
      data-oid="i:6gdy3"
    >
      <div className="w-full h-full relative" data-oid="rzcgscc">
        <InfiniteCanvas
          mode={mode}
          defaultView={view}
          onViewChange={setView}
          onModeChange={setMode}
          data-oid="wvibi5o"
        />

        <div className="absolute top-4 left-4 z-10" data-oid="ua5p7li">
          <Toolbar mode={mode} onModeChange={setMode} data-oid="m_gob9o" />
        </div>
        <div className="absolute top-4 right-4 z-10" data-oid="hk8zope">
          <ViewSelector
            currentView={view}
            onViewChange={setView}
            data-oid="7kdma-u"
          />
        </div>
      </div>
    </CanvasProvider>
  );
}

const root = document.getElementById("root");
if (root) {
  ReactDOM.createRoot(root).render(
    <React.StrictMode data-oid="mj.fdhe">
      <Demo data-oid="c-gcqhy" />
    </React.StrictMode>,
  );
}
