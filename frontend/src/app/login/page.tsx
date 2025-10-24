import Image from "next/image";
import Link from "next/link";
import { Inter } from "next/font/google";
import { FormSignIn } from "./form"

export const metadata = {
    title: "Entrar — Task",

};

const inter = Inter({ subsets: ["latin"], display: "swap" });


export default function Login() {
    return (
        <main
            className={`${inter.className} mx-auto min-h-dvh  bg-white text-gray-900`}
        >
            <section
                aria-labelledby="register-title"
                className="grid min-h-dvh grid-cols-1 md:grid-cols-2"
            >
                {/* Painel ilustrado (esquerda) */}
                <div className="relative hidden overflow-hidden rounded-none bg-[#6FA4FF] md:block md:rounded-r-3xl">
                    <span className="sr-only">
                        Painel ilustrado com cenário de tarefas.
                    </span>
                    <div className="absolute inset-0 p-16">
                        <div className="relative mx-auto h-full max-w-[640px]">
                            <Image
                                src="/add-tasks-cuate.svg"
                                alt="Ilustração de pessoa marcando tarefas em um bloco de notas, representando organização de tarefas."
                                fill
                                priority
                                sizes="(min-width: 1024px) 42vw, 100vw"
                                className="object-contain"
                            />
                        </div>
                    </div>
                </div>

                {/* Formulário (direita) */}
                <div className="flex items-center justify-center px-6 py-12 md:px-12">
                    <div className="w-full max-w-xl">
                        <header className="text-center">
                            <h1
                                id="register-title"
                                className="text-2xl font-bold tracking-tight text-gray-900 md:text-4xl"
                            >
                                Organize suas tarefas de forma fácil e rápida
                            </h1>

                        </header>

                        <FormSignIn />
                    </div>
                </div>
            </section>
        </main>
    );
}
