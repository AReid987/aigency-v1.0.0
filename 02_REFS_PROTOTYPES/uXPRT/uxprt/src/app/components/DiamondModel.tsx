import React, { useRef, Suspense, useMemo, useEffect } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import {
  OrbitControls,
  useGLTF,
  Environment,
  Points,
  PointMaterial,
} from "@react-three/drei";
import * as THREE from "three";

// Helper function to generate jagged line segments
function generateJaggedSegments(
  start: THREE.Vector3,
  end: THREE.Vector3,
  numSegments: number,
  jaggedness: number
): Array<{ from: THREE.Vector3; to: THREE.Vector3 }> {
  const segments: Array<{ from: THREE.Vector3; to: THREE.Vector3 }> = [];
  let lastJaggedPoint = start.clone();
  const mainDirection = end.clone().sub(start);
  const mainLength = mainDirection.length();

  if (mainLength < 0.0001) {
    // If start and end are virtually the same
    segments.push({ from: start.clone(), to: end.clone() });
    return segments;
  }
  mainDirection.normalize();

  for (let s = 0; s < numSegments; s++) {
    const t = (s + 1) / numSegments;
    const idealPointOnLine = start.clone().lerp(end, t);

    let displacementDirection = new THREE.Vector3().randomDirection();

    // Make displacementDirection perpendicular to mainDirection
    const projectOnMain = mainDirection
      .clone()
      .multiplyScalar(displacementDirection.dot(mainDirection));
    displacementDirection.sub(projectOnMain).normalize();

    if (displacementDirection.lengthSq() < 0.5) {
      // If it became near zero (was parallel)
      if (Math.abs(mainDirection.x) < 0.9 && Math.abs(mainDirection.y) < 0.9) {
        // If not primarily along Z
        displacementDirection
          .set(-mainDirection.y, mainDirection.x, 0)
          .normalize(); // Perpendicular in XY plane
      } else if (
        Math.abs(mainDirection.y) < 0.9 &&
        Math.abs(mainDirection.z) < 0.9
      ) {
        // If not primarily along X
        displacementDirection
          .set(0, -mainDirection.z, mainDirection.y)
          .normalize(); // Perpendicular in YZ plane
      } else {
        // If not primarily along Y (or if other checks failed)
        displacementDirection
          .set(mainDirection.z, 0, -mainDirection.x)
          .normalize(); // Perpendicular in XZ plane
      }

      if (displacementDirection.lengthSq() < 0.5) {
        // Final fallback if still zero
        displacementDirection.set(1, 0, 0); // Default to X if mainDirection was (0,0,0) or specific alignments
        // Check if mainDirection is parallel to X, then use Y
        if (Math.abs(mainDirection.dot(new THREE.Vector3(1, 0, 0))) > 0.99) {
          displacementDirection.set(0, 1, 0);
        }
      }
    }

    const displacementMagnitude =
      (mainLength / numSegments) * jaggedness * (Math.random() * 0.7 + 0.3); // Randomize displacement a bit

    const displacedPoint = idealPointOnLine.add(
      displacementDirection.multiplyScalar(displacementMagnitude)
    );

    segments.push({
      from: lastJaggedPoint.clone(),
      to: displacedPoint.clone(),
    });
    lastJaggedPoint = displacedPoint.clone();
  }
  // Ensure the hop connects to the actual end point
  segments.push({ from: lastJaggedPoint.clone(), to: end.clone() });
  return segments;
}

interface ModelProps {
  url: string;
}

function Model({ url }: ModelProps) {
  const { scene } = useGLTF(url);
  const modelRef = useRef<THREE.Group>(null!);

  useFrame((_state, delta) => {
    if (modelRef.current) {
      modelRef.current.rotation.y += delta * 0.3; // Slow rotation
    }
  });

  return (
    <primitive
      ref={modelRef}
      object={scene}
      scale={1.5}
      position={[0, 0.2, 0]}
      renderOrder={1} // Ensure diamond renders after particles
    />
  );
}

useGLTF.preload("/xprt-blue-diamond.glb");

const ParticleGround: React.FC = () => {
  const pointsRef = useRef<THREE.Points>(null!);
  const numParticles = 8000;
  const particleSize = 0.06; // Keep larger particles
  const areaSize = 18; // Total diameter of the particle area
  const startY = -3.0; // Particles start from below
  const riseLimitY = 3.0; // Particles reset above this Y

  // Constants for new density gradient
  const DIAMOND_CENTER_XZ_RADIUS_EQUIVALENT = 1.0; // World units for high-density area radius
  const PARTICLE_CONCENTRATION_RATIO_CENTER = 0.5; // 50% of particles in the high-density area
  const OUTER_DENSITY_FALLOFF_EXPONENT = 1.5; // Exponent > 1 biases outer particles closer to the inner radius

  const numInnerParticles = Math.floor(
    numParticles * PARTICLE_CONCENTRATION_RATIO_CENTER
  );

  const particleAttributes = useMemo(() => {
    const positions = new Float32Array(numParticles * 3);
    const baseColors = new Float32Array(numParticles * 3); // Renamed for clarity
    const liveColors = new Float32Array(numParticles * 3); // For dynamic glow
    const randomFactors = new Float32Array(numParticles * 3);

    const centerColor = new THREE.Color("#5627b0"); // Accent Purple
    const edgeColor = new THREE.Color("#27b08b"); // Primary Green
    const tempColor = new THREE.Color();
    const maxDistanceColorInterpolation = areaSize / 2.2; // For color interpolation

    for (let i = 0; i < numParticles; i++) {
      const i3 = i * 3;
      const angle = Math.random() * Math.PI * 2;
      // Initial particle distribution:
      // Goal: Avoid dense vertical column around (0,Y,0) on page load.
      // Particles should start in a more diffuse XZ pattern.
      const initialDistMinRadius = 1.5; // Min XZ distance from Y-axis for initial spawn
      const initialDistMaxRadius = areaSize / 2; // Max XZ distance, outer edge of the particle area

      // Ensure initialDistMinRadius is safely less than initialDistMaxRadius.
      // Subtract a small epsilon to ensure the range is valid if min and max are very close or equal.
      const safeInitialMinRadius = Math.min(
        initialDistMinRadius,
        initialDistMaxRadius - 0.01
      );

      // Use sqrt(random) to bias particles towards the outer parts of this initial ring,
      // promoting a more diffuse appearance.
      const randomFactorForInitialRadius = Math.sqrt(Math.random());
      // Ensure the range (initialDistMaxRadius - safeInitialMinRadius) is non-negative before multiplication
      const radiusRange = Math.max(
        0,
        initialDistMaxRadius - safeInitialMinRadius
      );
      const initialEffectiveRadius =
        safeInitialMinRadius + randomFactorForInitialRadius * radiusRange;

      const x = Math.cos(angle) * initialEffectiveRadius; // 'angle' is defined before this block
      const z = Math.sin(angle) * initialEffectiveRadius;

      positions[i3 + 0] = x;
      positions[i3 + 1] = startY + Math.random() * (riseLimitY - startY); // Y remains uniform for initial spread
      positions[i3 + 2] = z;

      const distance = Math.sqrt(x * x + z * z);
      const lerpFactor = Math.min(1, distance / maxDistanceColorInterpolation);
      tempColor.copy(centerColor).lerp(edgeColor, lerpFactor);

      baseColors[i3 + 0] = tempColor.r;
      baseColors[i3 + 1] = tempColor.g;
      baseColors[i3 + 2] = tempColor.b;

      liveColors[i3 + 0] = tempColor.r;
      liveColors[i3 + 1] = tempColor.g;
      liveColors[i3 + 2] = tempColor.b;

      randomFactors[i3 + 0] = Math.random() * 0.5 + 0.5; // x-meander speed factor
      randomFactors[i3 + 1] = Math.random() * Math.PI * 2; // meander phase
      randomFactors[i3 + 2] = Math.random() * 0.5 + 0.5; // z-meander speed factor
    }
    return { positions, baseColors, liveColors, randomFactors };
  }, [
    numParticles,
    areaSize,
    startY,
    riseLimitY,
    numInnerParticles, // Added dependency
    DIAMOND_CENTER_XZ_RADIUS_EQUIVALENT,
    OUTER_DENSITY_FALLOFF_EXPONENT,
  ]);

  useEffect(() => {
    if (pointsRef.current) {
      pointsRef.current.geometry.setAttribute(
        "color",
        new THREE.BufferAttribute(particleAttributes.liveColors, 3)
      );
    }
  }, [particleAttributes.liveColors]);

  // Removed animeInstance state and useEffect hooks for animejs v4.0.2
  // as it was causing persistent internal errors ("keyframes").
  // The particle animation originally intended with animejs is currently not active.

  const riseSpeed = 0.0005;
  const meanderStrength = 0.0005;
  const meanderBaseSpeed = 0.01;
  const opacityPulseSpeed = 0.05;
  const minOpacity = 0.1; // Base min opacity
  const maxOpacity = 0.6; // Base max opacity
  const fadeEdgeFactor = 0.2; // How much of the top/bottom area is used for fading

  const sparkLinesRef = useRef<THREE.LineSegments>(null!);
  const activeStrikes = useRef<
    Array<{
      id: number;
      segments: Array<{ from: THREE.Vector3; to: THREE.Vector3 }>;
      particlesHitIndices: number[];
      life: number;
    }>
  >([]);
  const particleGlows = useRef<{
    [particleIndex: number]: { startTime: number };
  }>({});
  const nextStrikeId = useRef(0);
  const lastSparkTime = useRef(0);

  const SPARK_INTERVAL = 2.5; // Less frequent: Increased from 1.2
  const MAX_ACTIVE_STRIKES = 1;
  const STRIKE_HOPS_MIN = 2;
  const STRIKE_HOPS_MAX = 12; // Quadrupled from 3 for much longer strikes
  const HOP_MAX_DISTANCE = 1.2; // Reduced from areaSize / 3 (which was 6)
  const STRIKE_LIFESPAN = 4.0; // Data lifetime for strike, also affects particle glow
  const VISIBLE_STRIKE_DURATION = 0.15; // Total time the lightning flash is visible (decreased from 0.3)
  const STRIKE_RAMP_UP_TIME = 0.05; // Time for strike to reach full brightness
  const STRIKE_HOLD_TIME = 0.1; // Time strike stays at full brightness
  // STRIKE_FADE_OUT_TIME is derived from the above: VISIBLE_STRIKE_DURATION - RAMP_UP - HOLD
  const SEGMENTS_PER_HOP_MIN = 3;
  const SEGMENTS_PER_HOP_MAX = 7; // Increased from 5 to 7 for more detail
  const JAGGEDNESS_FACTOR = 0.6; // Increased from 0.35 to 0.6 for more erratic paths
  const SPARK_COLOR = 0xd0f0ff; // Changed from 0xeeeeff for a lighter cyan/white glow
  const PARTICLE_GLOW_DURATION = STRIKE_LIFESPAN * 0.8;
  const PARTICLE_GLOW_INTENSITY_ADD = 1.2; // Increased from 0.7 to 1.2 for brighter particle glow

  // Branching constants
  const BRANCH_CHANCE_PER_HOP = 0.45; // 45% chance a main hop will spawn branches
  const BRANCHES_PER_HOP_MIN = 1;
  const BRANCHES_PER_HOP_MAX = 2;
  const BRANCH_SEGMENTS_MIN = 2;
  const BRANCH_SEGMENTS_MAX = 4;
  const BRANCH_LENGTH_FACTOR = 0.65; // Branch length relative to its parent hop segment's length
  const BRANCH_ANGLE_VARIATION = Math.PI / 2.5; // Max deviation from parent segment direction (radians) ~72deg

  useFrame((state, delta) => {
    if (
      !pointsRef.current ||
      !pointsRef.current.material ||
      !sparkLinesRef.current
    )
      return;

    const livePositions = pointsRef.current.geometry.attributes.position
      .array as Float32Array;
    const { baseColors, randomFactors } = particleAttributes;
    const liveColors = (
      pointsRef.current.geometry.attributes.color as THREE.BufferAttribute
    ).array as Float32Array;
    const time = state.clock.elapsedTime;

    for (let i = 0; i < numParticles; i++) {
      const i3 = i * 3;

      livePositions[i3 + 1] += riseSpeed;

      const rfxSpeed = randomFactors[i3 + 0];
      const rfxPhase = randomFactors[i3 + 1];
      const rfzSpeed = randomFactors[i3 + 2];

      livePositions[i3] +=
        Math.sin(time * rfxSpeed * meanderBaseSpeed + rfxPhase) *
        meanderStrength;
      livePositions[i3 + 2] +=
        Math.cos(time * rfzSpeed * meanderBaseSpeed + rfxPhase * 0.5) *
        meanderStrength;

      if (livePositions[i3 + 1] > riseLimitY) {
        livePositions[i3 + 1] = startY; // Reset Y position

        // Apply new density distribution on reset
        const resetAngle = Math.random() * Math.PI * 2;
        let resetRadius;
        if (i < numInnerParticles) {
          resetRadius =
            DIAMOND_CENTER_XZ_RADIUS_EQUIVALENT * Math.sqrt(Math.random());
        } else {
          resetRadius =
            DIAMOND_CENTER_XZ_RADIUS_EQUIVALENT +
            (areaSize / 2 - DIAMOND_CENTER_XZ_RADIUS_EQUIVALENT) *
              Math.pow(Math.random(), OUTER_DENSITY_FALLOFF_EXPONENT);
        }
        livePositions[i3] = Math.cos(resetAngle) * resetRadius; // New X
        livePositions[i3 + 2] = Math.sin(resetAngle) * resetRadius; // New Z
      }
    }
    pointsRef.current.geometry.attributes.position.needsUpdate = true;

    // Opacity calculation with edge fade
    const currentGlobalOpacity =
      minOpacity +
      (maxOpacity - minOpacity) *
        ((Math.sin(time * opacityPulseSpeed) + 1) / 2);

    // let totalOpacity = 0; // This was for a potential average, not used directly
    for (let i = 0; i < numParticles; i++) {
      const i3 = i * 3;
      const yPos = livePositions[i3 + 1];
      let edgeOpacityMultiplier = 1.0;
      const fadeRange = (riseLimitY - startY) * fadeEdgeFactor;

      if (yPos < startY + fadeRange) {
        edgeOpacityMultiplier = (yPos - startY) / fadeRange;
      } else if (yPos > riseLimitY - fadeRange) {
        edgeOpacityMultiplier = (riseLimitY - yPos) / fadeRange;
      }
      edgeOpacityMultiplier = THREE.MathUtils.clamp(
        edgeOpacityMultiplier,
        0.05,
        1.0
      ); // Ensure a minimum visibility
      // totalOpacity += currentGlobalOpacity * edgeOpacityMultiplier;

      // XZ distance-based fading
      const xzDistance = Math.sqrt(
        livePositions[i3] * livePositions[i3] +
          livePositions[i3 + 2] * livePositions[i3 + 2]
      );
      const xzOpacityFalloffStart = DIAMOND_CENTER_XZ_RADIUS_EQUIVALENT;
      const xzOpacityFalloffEnd = areaSize / 2;
      let xzDistanceFactor = 1.0;

      if (xzDistance > xzOpacityFalloffStart) {
        xzDistanceFactor =
          1.0 -
          THREE.MathUtils.clamp(
            (xzDistance - xzOpacityFalloffStart) /
              (xzOpacityFalloffEnd - xzOpacityFalloffStart),
            0,
            1
          );
        xzDistanceFactor = Math.pow(xzDistanceFactor, 2); // Sharper falloff
      }
      xzDistanceFactor = Math.max(0.05, xzDistanceFactor); // Ensure minimum visibility for XZ fade

      const particleBaseColor = new THREE.Color(
        baseColors[i3],
        baseColors[i3 + 1],
        baseColors[i3 + 2]
      );
      const fadedColor = particleBaseColor
        .clone()
        .multiplyScalar(edgeOpacityMultiplier * xzDistanceFactor); // Combined Y and XZ fading

      const glowData = particleGlows.current[i];
      if (glowData) {
        const elapsedGlowTime = time - glowData.startTime;
        if (elapsedGlowTime < PARTICLE_GLOW_DURATION) {
          const glowProgress = 1 - elapsedGlowTime / PARTICLE_GLOW_DURATION;
          const currentGlow = PARTICLE_GLOW_INTENSITY_ADD * glowProgress;
          // Apply glow to the faded color
          liveColors[i3 + 0] = Math.min(1.0, fadedColor.r + currentGlow);
          liveColors[i3 + 1] = Math.min(1.0, fadedColor.g + currentGlow);
          liveColors[i3 + 2] = Math.min(1.0, fadedColor.b + currentGlow);
        } else {
          // No glow, just the faded color
          liveColors[i3 + 0] = fadedColor.r;
          liveColors[i3 + 1] = fadedColor.g;
          liveColors[i3 + 2] = fadedColor.b;
          delete particleGlows.current[i];
        }
      } else {
        // No glow, just the faded color
        liveColors[i3 + 0] = fadedColor.r;
        liveColors[i3 + 1] = fadedColor.g;
        liveColors[i3 + 2] = fadedColor.b;
      }
    }
    (pointsRef.current.material as THREE.PointsMaterial).opacity =
      currentGlobalOpacity; // Set the global opacity
    (
      pointsRef.current.geometry.attributes.color as THREE.BufferAttribute
    ).needsUpdate = true;

    activeStrikes.current = activeStrikes.current
      .map((strike) => ({ ...strike, life: strike.life - delta }))
      .filter((strike) => strike.life > 0);

    if (
      activeStrikes.current.length < MAX_ACTIVE_STRIKES &&
      time - lastSparkTime.current > SPARK_INTERVAL
    ) {
      const startIdx = Math.floor(Math.random() * numParticles);
      let currentPoint = new THREE.Vector3().fromBufferAttribute(
        pointsRef.current.geometry.attributes.position,
        startIdx
      );

      const currentStrikeParticlesHit: number[] = [startIdx];
      const currentStrikeSegments: Array<{
        from: THREE.Vector3;
        to: THREE.Vector3;
      }> = [];
      const numHops =
        Math.floor(Math.random() * (STRIKE_HOPS_MAX - STRIKE_HOPS_MIN + 1)) +
        STRIKE_HOPS_MIN;

      for (let hop = 0; hop < numHops; hop++) {
        let nextHopIdx = -1;
        const potentialNextHops: number[] = [];

        for (let j = 0; j < numParticles; j++) {
          if (currentStrikeParticlesHit.includes(j)) continue;
          const p_candidate = new THREE.Vector3().fromBufferAttribute(
            pointsRef.current.geometry.attributes.position,
            j
          );
          const dist = currentPoint.distanceTo(p_candidate);
          if (dist < HOP_MAX_DISTANCE && dist > 0.1) {
            // Ensure some minimum distance for a hop
            potentialNextHops.push(j);
          }
        }

        if (potentialNextHops.length > 0) {
          nextHopIdx =
            potentialNextHops[
              Math.floor(Math.random() * potentialNextHops.length)
            ];
        } else {
          break; // No suitable next hop found
        }

        const mainHopStart = currentPoint.clone();
        const mainHopEnd = new THREE.Vector3().fromBufferAttribute(
          pointsRef.current.geometry.attributes.position,
          nextHopIdx
        );

        const numMainJaggedSegments =
          Math.floor(
            Math.random() * (SEGMENTS_PER_HOP_MAX - SEGMENTS_PER_HOP_MIN + 1)
          ) + SEGMENTS_PER_HOP_MIN;
        const mainHopSegments = generateJaggedSegments(
          mainHopStart,
          mainHopEnd,
          numMainJaggedSegments,
          JAGGEDNESS_FACTOR
        );
        currentStrikeSegments.push(...mainHopSegments);

        // --- Branching Logic ---
        if (Math.random() < BRANCH_CHANCE_PER_HOP) {
          const numBranchesToSpawn =
            Math.floor(
              Math.random() * (BRANCHES_PER_HOP_MAX - BRANCHES_PER_HOP_MIN + 1)
            ) + BRANCHES_PER_HOP_MIN;

          for (let b = 0; b < numBranchesToSpawn; b++) {
            const branchOrigin = mainHopStart
              .clone()
              .lerp(mainHopEnd, Math.random() * 0.8 + 0.1); // Branch from a point along the main hop (not too close to ends)

            const mainHopDirectionVec = mainHopEnd.clone().sub(mainHopStart);
            const mainHopActualLength = mainHopDirectionVec.length();
            if (mainHopActualLength < 0.001) continue; // Skip branching for zero-length main hops
            mainHopDirectionVec.normalize();

            let randomRotationAxis = new THREE.Vector3().randomDirection();
            const projectOnMain = mainHopDirectionVec
              .clone()
              .multiplyScalar(randomRotationAxis.dot(mainHopDirectionVec));
            randomRotationAxis.sub(projectOnMain).normalize();

            if (randomRotationAxis.lengthSq() < 0.5) {
              if (
                Math.abs(mainHopDirectionVec.x) < 0.9 &&
                Math.abs(mainHopDirectionVec.y) < 0.9
              ) {
                randomRotationAxis
                  .set(-mainHopDirectionVec.y, mainHopDirectionVec.x, 0)
                  .normalize();
              } else if (
                Math.abs(mainHopDirectionVec.y) < 0.9 &&
                Math.abs(mainHopDirectionVec.z) < 0.9
              ) {
                randomRotationAxis
                  .set(0, -mainHopDirectionVec.z, mainHopDirectionVec.y)
                  .normalize();
              } else {
                randomRotationAxis
                  .set(mainHopDirectionVec.z, 0, -mainHopDirectionVec.x)
                  .normalize();
              }
              if (randomRotationAxis.lengthSq() < 0.5)
                randomRotationAxis.set(0, 1, 0); // Ultimate fallback
            }

            const randomAngle =
              (Math.random() - 0.5) * 2 * BRANCH_ANGLE_VARIATION;
            const branchDirection = mainHopDirectionVec
              .clone()
              .applyAxisAngle(randomRotationAxis, randomAngle);

            const branchLength =
              mainHopActualLength *
              BRANCH_LENGTH_FACTOR *
              (Math.random() * 0.6 + 0.4); // Randomize length a bit more
            const branchTarget = branchOrigin
              .clone()
              .add(branchDirection.multiplyScalar(branchLength));

            const numBranchJaggedSegments =
              Math.floor(
                Math.random() * (BRANCH_SEGMENTS_MAX - BRANCH_SEGMENTS_MIN + 1)
              ) + BRANCH_SEGMENTS_MIN;
            const branchSegments = generateJaggedSegments(
              branchOrigin,
              branchTarget,
              numBranchJaggedSegments,
              JAGGEDNESS_FACTOR * 0.8
            ); // Slightly less jagged branches
            currentStrikeSegments.push(...branchSegments);
          }
        }
        // --- End Branching Logic ---

        currentStrikeParticlesHit.push(nextHopIdx);
        currentPoint = mainHopEnd.clone(); // Move to the end of the main hop for the next main hop
      }

      if (currentStrikeSegments.length > 0) {
        activeStrikes.current.push({
          id: nextStrikeId.current++,
          segments: currentStrikeSegments,
          particlesHitIndices: currentStrikeParticlesHit,
          life: STRIKE_LIFESPAN,
        });
        currentStrikeParticlesHit.forEach((idx) => {
          particleGlows.current[idx] = { startTime: time };
        });
      }
      lastSparkTime.current = time;
    }

    const sparkVertices = [];
    let maxStrikeOpacity = 0;

    if (activeStrikes.current.length > 0) {
      // Assuming MAX_ACTIVE_STRIKES = 1, so we operate on the first strike for opacity
      const strike = activeStrikes.current[0];
      const age = STRIKE_LIFESPAN - strike.life; // Time since strike was born

      let currentStrikeOpacity = 0;
      const strikeFadeOutTime =
        VISIBLE_STRIKE_DURATION - STRIKE_RAMP_UP_TIME - STRIKE_HOLD_TIME;

      if (age < STRIKE_RAMP_UP_TIME) {
        currentStrikeOpacity = age / STRIKE_RAMP_UP_TIME;
      } else if (age < STRIKE_RAMP_UP_TIME + STRIKE_HOLD_TIME) {
        currentStrikeOpacity = 1.0;
      } else if (age < VISIBLE_STRIKE_DURATION && strikeFadeOutTime > 0) {
        const fadeElapsedTime = age - (STRIKE_RAMP_UP_TIME + STRIKE_HOLD_TIME);
        currentStrikeOpacity = 1.0 - fadeElapsedTime / strikeFadeOutTime;
      } else {
        currentStrikeOpacity = 0; // Strike has faded or fade duration is invalid
      }
      maxStrikeOpacity = THREE.MathUtils.clamp(currentStrikeOpacity, 0, 1);

      // Populate sparkVertices only if the strike is potentially visible
      if (maxStrikeOpacity > 0) {
        for (const segment of strike.segments) {
          sparkVertices.push(segment.from.x, segment.from.y, segment.from.z);
          sparkVertices.push(segment.to.x, segment.to.y, segment.to.z);
        }
      }
    }

    if (sparkLinesRef.current) {
      (sparkLinesRef.current.material as THREE.LineBasicMaterial).opacity =
        maxStrikeOpacity;
      if (sparkVertices.length > 0 && maxStrikeOpacity > 0) {
        sparkLinesRef.current.geometry.setAttribute(
          "position",
          new THREE.Float32BufferAttribute(sparkVertices, 3)
        );
      } else {
        // Set to empty if no vertices or fully faded to avoid rendering old strike
        sparkLinesRef.current.geometry.setAttribute(
          "position",
          new THREE.Float32BufferAttribute([], 3)
        );
      }
      sparkLinesRef.current.geometry.attributes.position.needsUpdate = true;
    }
  });

  return (
    <group>
      {/* testDivRef and its div removed */}
      <Points
        ref={pointsRef}
        positions={particleAttributes.positions}
        stride={3}
        frustumCulled={false}
        renderOrder={0} // Ensure particles render before the diamond
      >
        <PointMaterial
          transparent
          size={particleSize}
          sizeAttenuation={true}
          depthWrite={false}
          opacity={minOpacity}
          vertexColors={true}
          blending={THREE.AdditiveBlending}
        />
      </Points>
      <lineSegments ref={sparkLinesRef} frustumCulled={false}>
        <lineBasicMaterial
          attach='material'
          color={SPARK_COLOR}
          transparent
          opacity={0}
          blending={THREE.AdditiveBlending}
          linewidth={1.0} // Adjusted for a thinner, fuzzier glow (was 20.0)
        />
      </lineSegments>
    </group>
  );
};

const DiamondModel: React.FC = () => {
  return (
    <div className='w-full h-full absolute inset-0 z-0'>
      <Canvas camera={{ position: [0, 1, 5], fov: 50 }}>
        <ambientLight intensity={0.5} />
        <directionalLight position={[10, 10, 5]} intensity={1} />
        <directionalLight position={[-10, -10, -5]} intensity={0.5} />

        <Suspense fallback={null}>
          <Model url='/xprt-blue-diamond.glb' />
          <Environment preset='sunset' />
          <ParticleGround />
        </Suspense>

        <OrbitControls
          enableZoom={false}
          enablePan={false}
          minPolarAngle={Math.PI / 3}
          maxPolarAngle={Math.PI / 2.2}
        />
      </Canvas>
    </div>
  );
};

export default DiamondModel;
