import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';

const Canvas3D = () => {
  return (
    <div className="w-full h-full">
      <Canvas camera={{ position: [3, 3, 3], fov: 75 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} />
        <OrbitControls />
        <mesh>
          <boxGeometry args={[1, 1, 1]} />
          <meshStandardMaterial color="orange" />
        </mesh>
      </Canvas>
    </div>
  );
};

export default Canvas3D;