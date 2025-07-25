import React from 'react';
import Image, { type ImageProps } from "next/image";
import { Button } from "@repo/ui/button";
import styles from "./page.module.css";

type Props = Omit<ImageProps, "src"> & {
  srcLight: string;
  srcDark: string;
};

const ThemeImage = (props: Props) => {
  const { srcLight, srcDark, ...rest } = props;

  return (
    <>
      <Image {...rest} src={srcLight} className="imgLight" data-oid="ap:a6_y" />
      <Image {...rest} src={srcDark} className="imgDark" data-oid="6gq4lic" />
    </>
  );
};

interface HomePageProps {}

export default function Home({}: HomePageProps) {
  return (
    <div className={styles.page} data-oid="r5h47l8">
      <main className={styles.main} data-oid="cyg1jqs">
        <ThemeImage
          className={styles.logo}
          srcLight="turborepo-dark.svg"
          srcDark="turborepo-light.svg"
          alt="Turborepo logo"
          width={180}
          height={38}
          priority
          data-oid="rrtbwp8"
        />

        <ol data-oid="z0suk9s">
          <li data-oid="livxtlm">
            Get started by editing{" "}
            <code data-oid="4gacrin">apps/docs/app/page.tsx</code>
          </li>
          <li data-oid="zuj44_z">Save and see your changes instantly.</li>
        </ol>

        <div className={styles.ctas} data-oid="4ytjwyr">
          <a
            className={styles.primary}
            href="https://vercel.com/new/clone?demo-description=Learn+to+implement+a+monorepo+with+a+two+Next.js+sites+that+has+installed+three+local+packages.&demo-image=%2F%2Fimages.ctfassets.net%2Fe5382hct74si%2F4K8ZISWAzJ8X1504ca0zmC%2F0b21a1c6246add355e55816278ef54bc%2FBasic.png&demo-title=Monorepo+with+Turborepo&demo-url=https%3A%2F%2Fexamples-basic-web.vercel.sh%2F&from=templates&project-name=Monorepo+with+Turborepo&repository-name=monorepo-turborepo&repository-url=https%3A%2F%2Fgithub.com%2Fvercel%2Fturborepo%2Ftree%2Fmain%2Fexamples%2Fbasic&root-directory=apps%2Fdocs&skippable-integrations=1&teamSlug=vercel&utm_source=create-turbo"
            target="_blank"
            rel="noopener noreferrer"
            data-oid="lr703at"
          >
            <Image
              className={styles.logo}
              src="/vercel.svg"
              alt="Vercel logomark"
              width={20}
              height={20}
              data-oid="ihucnzg"
            />
            Deploy now
          </a>
          <a
            href="https://turborepo.com/docs?utm_source"
            target="_blank"
            rel="noopener noreferrer"
            className={styles.secondary}
            data-oid="f7vn..g"
          >
            Read our docs
          </a>
        </div>
        <Button appName="docs" className={styles.secondary} data-oid="zoy3vm-">
          Open alert
        </Button>
      </main>
      <footer className={styles.footer} data-oid="6.le_dr">
        <a
          href="https://vercel.com/templates?search=turborepo&utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
          data-oid=".pm:jta"
        >
          <Image
            aria-hidden
            src="/window.svg"
            alt="Window icon"
            width={16}
            height={16}
            data-oid="hy6.gdl"
          />
          Examples
        </a>
        <a
          href="https://turborepo.com?utm_source=create-turbo"
          target="_blank"
          rel="noopener noreferrer"
          data-oid="ewxor0k"
        >
          <Image
            aria-hidden
            src="/globe.svg"
            alt="Globe icon"
            width={16}
            height={16}
            data-oid="bf769as"
          />
          Go to turborepo.com →
        </a>
      </footer>
    </div>
  );
}
