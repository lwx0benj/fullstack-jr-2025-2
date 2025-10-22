// app/page.tsx
import Image from "next/image";
import Link from "next/link";
import { Inter } from "next/font/google";

export const metadata = {
    title: "Organize seu dia — Task",
    description:
        "Com o Task, gerenciar tarefas nunca foi tão simples. Mantenha o foco no que realmente importa.",
    openGraph: {
        title: "Organize seu dia — Task",
        description:
            "Gerencie tarefas com facilidade e alcance seus objetivos. Entre ou crie sua conta gratuitamente.",
        url: "/",
        type: "website",
    },
};

const inter = Inter({ subsets: ["latin"], display: "swap" });

function PrimaryButton({
    children,
    href,
    className = "",
}: {
    children: React.ReactNode;
    href: string;
    className?: string;
}) {
    return (
        <Link
            href={href}
            className={`inline-flex w-full items-center justify-center rounded-full bg-white px-6 py-3 text-base font-semibold text-[#1E5EFF] shadow-sm ring-1 ring-white/20 transition duration-200 hover:bg-white/95 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-white/70 focus-visible:ring-offset-[#6FA4FF] active:translate-y-px md:w-auto ${className}`}
        >
            {children}
        </Link>
    );
}

function SecondaryButton({
    children,
    href,
    className = "",
}: {
    children: React.ReactNode;
    href: string;
    className?: string;
}) {
    return (
        <Link
            href={href}
            className={`inline-flex w-full items-center justify-center rounded-full bg-[#2F6BFF] px-6 py-3 text-base font-semibold text-white shadow-sm ring-1 ring-black/10 transition duration-200 hover:bg-[#285EE3] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-white/80 focus-visible:ring-offset-[#6FA4FF] active:translate-y-px md:w-auto ${className}`}
        >
            {children}
        </Link>
    );
}

export default function Page() {
    return (
        <main
            className={`${inter.className} min-h-dvh bg-[#6FA4FF] text-white antialiased`}
        >
            {/* Conteúdo central */}
            <section
                aria-labelledby="hero-title"
                className="mx-auto grid grid-cols-1 items-center gap-10 px-6 py-10 md:min-h-dvh md:grid-cols-2 md:gap-12 md:px-10"
            >
                {/* Ilustração à esquerda */}
                <div className="relative order-2 mx-auto aspect-4/3 w-full max-w-[640px] md:order-1 md:aspect-5/4">
                    {/* Substitua /start-illustration.png por sua imagem local em public/ */}
                    <Image
                        src="/time-management-cuate.svg"
                        alt="Ilustração: pessoa em frente a um relógio, calendário e planta representando organização de tarefas."
                        fill
                        priority
                        sizes="(min-width: 1024px) 48vw, (min-width: 768px) 50vw, 100vw"
                        className="object-contain drop-shadow-md"
                    />
                </div>

                {/* Texto */}
                <div className="max-w-2xl order-1 md:order-2">
                    <h1
                        id="hero-title"
                        className="text-4xl font-extrabold leading-tight tracking-tight md:text-5xl"
                    >
                        <span className="block">Organize seu dia,</span>
                        <span className="block">alcance seus</span>
                        <span className="block">objetivos!</span>
                    </h1>

                    <p className="mt-6 max-w-[52ch] text-base/7 text-white/90 md:text-lg/8">
                        Com o Task, gerenciar tarefas nunca foi tão simples. Mantenha o foco
                        no que realmente importa.
                    </p>

                    <div className="mt-8 flex flex-col gap-3">
                        <PrimaryButton 
                            href="/login" 
                            className="rounded-lg" 
                            aria-label="Ir para a página de login"
                        >
                            Entrar
                        </PrimaryButton>
                        <SecondaryButton
                            href="/signup"
                            className="rounded-lg"
                            aria-label="Ir para a página de cadastro"
                        >
                            Cadastrar
                        </SecondaryButton>
                    </div>

                    <p className="mt-6 text-sm text-white/90">
                        Ainda não tem conta?{" "}
                        <Link
                            href="/signup"
                            className="underline decoration-white/60 underline-offset-4 hover:decoration-white"
                        >
                            Comece agora.
                        </Link>
                    </p>
                </div>
            </section>

            {/* Rodapé simples */}
            <footer className="border-t border-white/20 px-6 py-6 text-sm text-white/80 md:px-10">
                <div className="mx-auto flex max-w-7xl items-center justify-between">
                    <p>© {new Date().getFullYear()} Task</p>
                </div>
            </footer>
        </main>
    );
}
