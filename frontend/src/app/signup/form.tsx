"use client";

import Link from "next/link";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useRouter } from "next/navigation";

/** Schema de validação com Zod */
const signUpSchema = z
    .object({
        name: z
            .string()
            .min(2, "Informe pelo menos 2 caracteres.")
            .max(100, "Máximo de 100 caracteres."),
        email: z.string().email("Informe um e-mail válido."),
        password: z
            .string()
            .min(8, "A senha deve ter no mínimo 8 caracteres.")
            .regex(/[A-Z]/, "Inclua pelo menos 1 letra maiúscula.")
            .regex(/[a-z]/, "Inclua pelo menos 1 letra minúscula.")
            .regex(/[0-9]/, "Inclua pelo menos 1 número."),
        confirmPassword: z.string().min(8, "Confirme sua senha."),
    })
    .refine((data) => data.password === data.confirmPassword, {
        path: ["confirmPassword"],
        message: "As senhas não coincidem.",
    });

type SignUpForm = z.infer<typeof signUpSchema>;

export function FormSignUp() {
    const router = useRouter();
    const [errorMessage, setErrorMessage] = useState<string | null>(null);

    const {
        register,
        handleSubmit,
        formState: { errors, isSubmitting },
        reset,
    } = useForm<SignUpForm>({
        resolver: zodResolver(signUpSchema),
        mode: "onTouched",
    });

    const onSubmit = (data: SignUpForm) => {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL;

        return fetch(`${apiUrl}/api/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                name: data.name,
                email: data.email,
                password: data.password,
            }),
        })
            .then((response) =>
                response
                    .json()
                    .catch(() => ({}))
                    .then((body) => ({ status: response.status, body }))
            )
            .then(({ status }) =>
                status >= 200 && status < 300
                    ? Promise.resolve()
                    : Promise.reject()
            )
            .then(() => {
                setErrorMessage(null);
                reset();
                router.push("/login");
            })
            .catch(() => {
                setErrorMessage("Não foi possível finalizar o cadastro");
            });
    };

    return (
        <form
            className="mt-8 grid gap-4"
            aria-describedby="register-title"
            noValidate
            onSubmit={handleSubmit(onSubmit)}
        >
            {errorMessage && (
                <p className="text-base font-medium text-red-600 text-center">{errorMessage}</p>
            )}
            {/* Nome */}
            <div className="grid gap-2">
                <label htmlFor="name" className="text-sm font-medium text-gray-800">
                    Nome
                </label>
                <input
                    id="name"
                    placeholder="Nome"
                    autoComplete="given-name"
                    aria-invalid={!!errors.name}
                    className={[
                        "w-full rounded-xl border bg-white px-4 py-3 text-[15px] text-gray-900 shadow-sm outline-none transition placeholder:text-gray-400",
                        errors.name
                            ? "border-red-500 focus:border-red-500 focus:ring-4 focus:ring-red-500/20"
                            : "border-gray-300 focus:border-[#6FA4FF] focus:ring-4 focus:ring-[#6FA4FF]/25",
                    ].join(" ")}
                    {...register("name")}
                />
                {errors.name && (
                    <p className="text-xs font-medium text-red-600">{errors.name.message}</p>
                )}
            </div>

            {/* E-mail */}
            <div className="grid gap-2">
                <label htmlFor="email" className="text-sm font-medium text-gray-800">
                    E-mail
                </label>
                <input
                    id="email"
                    type="email"
                    placeholder="seuemail@exemplo.com"
                    autoComplete="email"
                    aria-invalid={!!errors.email}
                    className={[
                        "w-full rounded-xl border bg-white px-4 py-3 text-[15px] text-gray-900 shadow-sm outline-none transition placeholder:text-gray-400",
                        errors.email
                            ? "border-red-500 focus:border-red-500 focus:ring-4 focus:ring-red-500/20"
                            : "border-gray-300 focus:border-[#6FA4FF] focus:ring-4 focus:ring-[#6FA4FF]/25",
                    ].join(" ")}
                    {...register("email")}
                />
                {errors.email && (
                    <p className="text-xs font-medium text-red-600">{errors.email.message}</p>
                )}
            </div>

            {/* Senha */}
            <div className="grid gap-2">
                <label htmlFor="password" className="text-sm font-medium text-gray-800">
                    Senha
                </label>
                <input
                    id="password"
                    type="password"
                    placeholder="••••••••"
                    autoComplete="new-password"
                    aria-invalid={!!errors.password}
                    className={[
                        "w-full rounded-xl border bg-white px-4 py-3 text-[15px] text-gray-900 shadow-sm outline-none transition placeholder:text-gray-400",
                        errors.password
                            ? "border-red-500 focus:border-red-500 focus:ring-4 focus:ring-red-500/20"
                            : "border-gray-300 focus:border-[#6FA4FF] focus:ring-4 focus:ring-[#6FA4FF]/25",
                    ].join(" ")}
                    {...register("password")}
                />
                {errors.password && (
                    <p className="text-xs font-medium text-red-600">{errors.password.message}</p>
                )}
            </div>

            {/* Confirmar Senha */}
            <div className="grid gap-2">
                <label htmlFor="confirmPassword" className="text-sm font-medium text-gray-800">
                    Confirmar Senha
                </label>
                <input
                    id="confirmPassword"
                    type="password"
                    placeholder="••••••••"
                    autoComplete="new-password"
                    aria-invalid={!!errors.confirmPassword}
                    className={[
                        "w-full rounded-xl border bg-white px-4 py-3 text-[15px] text-gray-900 shadow-sm outline-none transition placeholder:text-gray-400",
                        errors.confirmPassword
                            ? "border-red-500 focus:border-red-500 focus:ring-4 focus:ring-red-500/20"
                            : "border-gray-300 focus:border-[#6FA4FF] focus:ring-4 focus:ring-[#6FA4FF]/25",
                    ].join(" ")}
                    {...register("confirmPassword")}
                />
                {errors.confirmPassword && (
                    <p className="text-xs font-medium text-red-600">
                        {errors.confirmPassword.message}
                    </p>
                )}
            </div>

            {/* Botão e erro geral */}
            <button
                type="submit"
                disabled={isSubmitting}
                className="mt-2 inline-flex w-full items-center justify-center rounded-2xl bg-[#6FA4FF] px-6 py-4 text-base font-semibold text-white shadow-sm transition duration-200 hover:bg-[#5B92F6] focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-[#6FA4FF]/40 active:translate-y-px disabled:opacity-60 disabled:cursor-not-allowed"
            >
                {isSubmitting ? "Enviando..." : "Cadastrar"}
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
    );
}
