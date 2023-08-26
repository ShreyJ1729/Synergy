import Image from "next/image";
import Navbar from "./navbar";
import Link from "next/link";

export default function Home() {
  const logos = ["/msft.webp", "/google.png", "/ibm.png"];
  return (
    <>
      <Navbar />
      <main className="flex flex-col items-center h-screen px-0 py-24 md:p-24">
        <div className="absolute -translate-y-1/4 -translate-x-20 h-[400px] w-[1000px] rounded-full bg-gradient-to-tr from-[#00306088] via-[#1b998b88] to-[#ade25d11] blur-[250px] content-[''] z-[-1]"></div>
        <div className="relative flex place-items-center">
          <h1 className="text-6xl font-semibold leading-snug text-center text-white">
            The{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#3bb9ab] to-[#ade25d]">
              Brainstorming Engine
            </span>
            <br /> You Can Talk To.
          </h1>
        </div>
        <div className="my-4 text-lg text-center text-gray-300">
          An AI-powered sounding board for all your thoughts.
        </div>
        <Link
          className="px-6 py-3 my-8 font-semibold text-black bg-yellow-300 rounded-full"
          href="/try"
        >
          Try It Now
        </Link>

        <p className="mt-16 text-left">Used by engineers at:</p>
        <div className="flex flex-col lg:flex-row justify-center mt-4 w-full grayscale-[75%]">
          {logos.map((logo) => (
            <div key={logo} className="m-auto my-4">
              <Image src={logo} alt={logo} width={150} height={10} />
            </div>
          ))}
        </div>
        {/* 
        <div className="grid text-center lg:mb-0 lg:grid-cols-4 lg:text-left">
          <a
            href="https://nextjs.org/docs?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
            className="px-5 py-4 transition-colors border border-transparent rounded-lg group hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
            target="_blank"
            rel="noopener noreferrer"
          >
            <img src="/msft.webp" width={64} height={64} />
            <h2 className={`mb-3 text-2xl font-semibold`}>
              Docs{" "}
              <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
                -&gt;
              </span>
            </h2>
            <p className={`m-0 max-w-[30ch] text-sm opacity-50`}>
              Find in-depth information about Next.js features and API.
            </p>
          </a>

          <a
            href="https://vercel.com/new?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
            className="px-5 py-4 transition-colors border border-transparent rounded-lg group hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
            target="_blank"
            rel="noopener noreferrer"
          >
            <h2 className={`mb-3 text-2xl font-semibold`}>
              Deploy{" "}
              <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
                -&gt;
              </span>
            </h2>
            <p className={`m-0 max-w-[30ch] text-sm opacity-50`}>
              Instantly deploy your Next.js site to a shareable URL with Vercel.
            </p>
          </a>
        </div> */}
      </main>
    </>
  );
}
