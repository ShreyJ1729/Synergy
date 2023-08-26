import Image from "next/image";

const Navbar = () => {
  return (
    <nav className="bg-transparent p-4 flex items-center justify-between mx-8">
      <div className="flex items-center">
        <Image
          src="/logo.png"
          alt="Logo"
          className="h-8 w-auto"
          width={100}
          height={100}
        />
        <span className="text-white text-xl font-semibold ml-2">Synergy</span>
      </div>
      <div className="space-x-8 hidden md:block">
        <a href="#" className="text-white hover:text-gray-300">
          Home
        </a>
        <a href="#" className="text-white hover:text-gray-300">
          Features
        </a>
        <a href="#" className="text-white hover:text-gray-300">
          Benefits
        </a>
        <a href="#" className="text-white hover:text-gray-300">
          FAQ
        </a>
        <a href="#" className="text-white hover:text-gray-300">
          Contact
        </a>
      </div>
    </nav>
  );
};

export default Navbar;
