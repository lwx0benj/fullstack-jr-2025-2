import Image from "next/image";
import Link from "next/link";
import { Inter } from "next/font/google";

export const metadata = {
    title: "Cadastro — Task",
};

const inter = Inter({ subsets: ["latin"], display: "swap" });

function Field({
    id,
    label,
    type = "text",
    placeholder,
    autoComplete,
}: {
    id: string;
    label: string;
    type?: string;
    placeholder?: string;
    autoComplete?: string;
}) {
    return (
        <div className="grid gap-2">
            <label htmlFor={id} className="text-sm font-medium text-gray-800">
                {label}
            </label>
            <input
                id={id}
                name={id}
                type={type}
                placeholder={placeholder}
                autoComplete={autoComplete}
                className="w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-[15px] text-gray-900 shadow-sm outline-none transition placeholder:text-gray-400 focus:border-[#6FA4FF] focus:ring-4 focus:ring-[#6FA4FF]/25"
            />
        </div>
    );
}

export default function SignUp() {
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
                            {/* Substitua por um arquivo em public/ com nome igual abaixo */}
                            <Image
                                src="/task-cuate.svg"
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
                                className="text-3xl font-extrabold tracking-tight text-gray-900 md:text-4xl"
                            >
                                Cadastro
                            </h1>
                            <p className="mt-2 text-sm text-gray-600">
                                Crie sua conta
                            </p>
                        </header>

                        <form
                            action="#"
                            method="post"
                            className="mt-8 grid gap-4"
                            aria-describedby="register-title"
                        >

                            <Field 
                                id="name" 
                                label="Nome" 
                                placeholder="Nome" 
                                autoComplete="given-name" 
                            />

                            <Field
                                id="email"
                                label="E-mail"
                                type="email"
                                placeholder="seuemail@exemplo.com"
                                autoComplete="email"
                            />

                            <Field
                                id="password"
                                label="Senha"
                                type="password"
                                placeholder="••••••••"
                                autoComplete="new-password"
                            />

                            <Field
                                id="confirmPassword"
                                label="Confirmar Senha"
                                type="password"
                                placeholder="••••••••"
                                autoComplete="new-password"
                            />

                            <button
                                type="submit"
                                className="mt-2 inline-flex w-full items-center justify-center rounded-2xl bg-[#6FA4FF] px-6 py-4 text-base font-semibold text-white shadow-sm transition duration-200 hover:bg-[#5B92F6] focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-[#6FA4FF]/40 active:translate-y-px"
                            >
                                Cadastrar
                            </button>

                            <div className="mt-4 flex items-center justify-between">
                                <p className="text-sm text-gray-600">
                                    Já possui conta? <span className="sr-only">Use o botão ao lado para entrar</span>
                                </p>
                                <Link
                                    href="/login"
                                    className="inline-flex items-center justify-center rounded-xl bg-gray-900 px-5 py-2.5 text-sm font-medium text-white shadow-sm transition hover:bg-gray-800 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-gray-900/30"
                                >
                                    Entrar
                                </Link>
                            </div>
                        </form>
                    </div>
                </div>
            </section>
        </main>
    );
}
