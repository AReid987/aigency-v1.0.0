import { useEffect, useRef } from 'react';
import * as THREE from 'three';

export const Hero = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Scene setup
    sceneRef.current = new THREE.Scene();
    cameraRef.current = new THREE.PerspectiveCamera(
      75,
      containerRef.current.clientWidth / containerRef.current.clientHeight,
      0.1,
      1000
    );

    rendererRef.current = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    rendererRef.current.setSize(
      containerRef.current.clientWidth,
      containerRef.current.clientHeight
    );
    containerRef.current.appendChild(rendererRef.current.domElement);

    // Create acrylic case
    const geometry = new THREE.BoxGeometry(2, 3, 0.1);
    const material = new THREE.MeshPhysicalMaterial({
      transparent: true,
      opacity: 0.4,
      roughness: 0.2,
      metalness: 0.1,
      clearcoat: 1.0,
      clearcoatRoughness: 0.1,
    });
    const case3D = new THREE.Mesh(geometry, material);
    sceneRef.current.add(case3D);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    sceneRef.current.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(5, 5, 5);
    sceneRef.current.add(directionalLight);

    cameraRef.current.position.z = 5;

    // Animation
    const animate = () => {
      requestAnimationFrame(animate);
      if (case3D && sceneRef.current && cameraRef.current && rendererRef.current) {
        case3D.rotation.y += 0.005;
        rendererRef.current.render(sceneRef.current, cameraRef.current);
      }
    };
    animate();

    // Cleanup
    return () => {
      if (containerRef.current && rendererRef.current) {
        containerRef.current.removeChild(rendererRef.current.domElement);
      }
    };
  }, []);

  return (
    <div className="relative h-screen w-full overflow-hidden">
      <div ref={containerRef} className="absolute inset-0" />
      <div className="relative z-10 container mx-auto px-6 h-full flex items-center">
        <div className="max-w-2xl">
          <h1 className="text-6xl font-bold text-neutral-dark mb-6">
            Miniature Art Curation
          </h1>
          <p className="text-xl text-neutral mb-8">
            Discover the beauty of miniature art pieces, carefully curated for collectors and enthusiasts.
          </p>
          <button className="bg-primary text-white px-8 py-3 rounded-md hover:bg-primary-dark transition-colors duration-200">
            Explore Collection
          </button>
        </div>
      </div>
    </div>
  );
};