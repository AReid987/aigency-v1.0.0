import Image, { type ImageProps } from "next/image";
import { Button } from "@xprt/ui/button";
import styles from "./page.module.css";

type Props = Omit<ImageProps, "src"> & {
  srcLight: string;
  srcDark: string;
};

export default function Home() {
  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <h1>devLog XPRT </h1>
        <Image
          src="/xprt-logomark.png"
          alt="devlog xprt logo"
          width={400}
          height={400}
        />
      </main>
    </div>
  );
}

export const metadata = {
  title: "devLog XPRT",
  description: "Knowledge OS",
};
