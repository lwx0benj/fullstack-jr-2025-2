"use client";

import { useState } from 'react';
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { de } from 'zod/locales';


const inter = Inter({ subsets: ["latin"] });


function PriorityPills({
    value,
    onChange,
}: {
    value: "Baixa" | "Média" | "Alta";
    onChange: (v: "Baixa" | "Média" | "Alta") => void;
}) {
    const map = {
        "Baixa": "bg-emerald-500 text-white",
        "Média": "bg-amber-400 text-white",
        "Alta": "bg-red-400 text-white",
    } as const;

    const all: Array<"Baixa" | "Média" | "Alta"> = ["Baixa", "Média", "Alta"];

    return (
        <div className="flex justify-start gap-8">
            {all.map((opt) => {
                const active = opt === value;
                return (
                    <button
                        key={opt}
                        type="button"
                        onClick={() => onChange(opt)}
                        className={[
                            "rounded-full px-3 py-1 text-base leading-5 ring-1 ring-gray-200 transition",
                            active
                                ? `${map[opt]}`
                                : "bg-gray-100 text-gray-700 hover:bg-white",
                        ].join(" ")}
                        aria-pressed={active}
                    >
                        {opt}
                    </button>
                );
            })}
        </div>
    );
}


function StatusBadges({
    value,
    onChange,
}: {
    value: "A Fazer" | "Em Progresso" | "Concluída";
    onChange: (v: "A Fazer" | "Em Progresso" | "Concluída") => void;
}) {
    const map = {
        "A Fazer": "bg-red-400 text-white",
        "Em Progresso": "bg-amber-400 text-white",
        Concluída: "bg-emerald-500 text-white",
    } as const;

    const all: Array<"A Fazer" | "Em Progresso" | "Concluída"> = [
        "A Fazer",
        "Em Progresso",
        "Concluída",
    ];

    return (
        <div className="flex gap-8">
            {all.map((opt) => {
                const active = opt === value;
                return (
                    <button
                        key={opt}
                        type="button"
                        onClick={() => onChange(opt)}
                        className={[
                            "rounded-full px-2 py-1 text-base leading-5 ring-1 ring-gray-200 transition",
                            active
                                ? `${map[opt]}`
                                : "bg-gray-100 text-gray-700 hover:bg-white",
                        ].join(" ")}
                        aria-pressed={active}
                    >
                        {opt}
                    </button>
                );
            })}
        </div>
    );
}


type ModalTaskProps = {
    open: boolean;               // controla abrir/fechar externamente
    onClose: () => void;         // callback para fechar
};

export function ModalTask({ open, onClose }: ModalTaskProps) {
    const [priority, setPriority] = useState<"Baixa" | "Média" | "Alta">("Alta");
    const [status, setStatus] = useState<"A Fazer" | "Em Progresso" | "Concluída">("A Fazer");

    if (!open) return null;

    return (
        // Overlay com blur e espaçamento responsivo nas bordas
        <div
            className="fixed inset-0 z-50 grid place-items-center bg-black/40 backdrop-blur-sm p-4 sm:p-6"
            role="presentation"
            aria-hidden={false}
            onClick={(e) => {
                // clique fora do dialog fecha
                if (e.target === e.currentTarget) onClose();
            }}
        >
            {/* Dialog responsivo: cresce até 3xl e respeita o viewport */}
            <section
                role="dialog"
                aria-modal="true"
                aria-labelledby="task-dialog-title"
                className={`${inter.className} relative w-full max-w-1/2 rounded-2xl bg-white  p-4 px-8 shadow-lg`}
            >
                {/* Fechar */}
                <button
                    onClick={onClose}
                    aria-label="Fechar"
                    className="absolute right-4 top-4 grid h-9 w-9 place-items-center rounded-full border border-gray-300 bg-white text-gray-700 transition hover:rotate-90 hover:bg-gray-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-400"
                >
                    <svg width="16" height="16" viewBox="0 0 24 24" role="img" aria-hidden="true">
                        <path d="M6 6l12 12M18 6L6 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                    </svg>
                </button>

                {/* Form */}
                <form
                    className="space-y-6 px-4 pr-8"
                    onSubmit={(e) => {
                        e.preventDefault();
                        alert("Tarefa salva!");
                    }}
                >
                    <div className="text-2xl font-bold text-gray-900" id="task-dialog-title">
                        Nova Tarefa
                    </div>
                    {/* Título: rótulo coluna fixa + campo fluido */}
                    <div className="grid-cols-1 items-center gap-3">
                        <label htmlFor="titulo" className="font-semibold text-gray-800 sm:text-lg">
                            Título
                        </label>
                        <input
                            id="titulo"
                            name="titulo"
                            placeholder="Ex.: Preparar apresentação de status"
                            className="h-10 w-full rounded-md border border-gray-300 bg-white px-3 text-[clamp(0.95rem,1vw,1rem)] leading-6 outline-none transition placeholder:text-gray-400 focus:ring-2 focus:ring-blue-500"
                            required
                        />
                    </div>

                    {/* Linha: Prioridade | Status (quebra para 1 col no mobile) */}
                    <div className="grid grid-cols-1 gap-2">
                        <div className="grid grid-cols-1 items-center gap-2">
                            <span className="font-semibold text-gray-800 sm:text-lg">Prioridade</span>
                            <PriorityPills value={priority} onChange={setPriority} />
                        </div>

                        <div className="grid items-center gap-2">
                            <span className="font-semibold text-gray-800 sm:text-lg">Status</span>
                            <StatusBadges value={status} onChange={setStatus} />
                        </div>
                    </div>

                    {/* Descrição ocupa toda a largura */}
                    <div className="grid gap-3 sm:grid-cols-1">
                        <label
                            htmlFor="descricao"
                            id="task-dialog-title"
                            className="text-base font-semibold text-gray-800 sm:text-lg self-start"
                        >
                            Descrição
                        </label>
                        <textarea
                            id="descricao"
                            name="descricao"
                            placeholder="Detalhe o que precisa ser feito, critérios de aceite, links, etc."
                            className="min-h-[120px] w-full resize-y rounded-md border border-gray-300 bg-white p-3 text-[15px] leading-6 outline-none transition placeholder:text-gray-400 focus:ring-2 focus:ring-blue-500"
                        />
                    </div>

                    {/* Ações: alinhar à direita em telas ≥ sm, empilhar no mobile */}
                    <div className="flex flex-col items-stretch gap-3 sm:flex-row sm:justify-end">
                        <button
                            type="button"
                            onClick={onClose}
                            className="inline-flex items-center justify-center rounded-md bg-neutral-900 px-5 py-2 text-sm font-semibold text-white shadow transition hover:bg-neutral-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-500 active:translate-y-1px"
                        >
                            Cancelar
                        </button>
                        <button
                            type="submit"
                            className="inline-flex items-center justify-center rounded-md bg-blue-500 px-5 py-2 text-sm font-semibold text-white shadow transition hover:bg-blue-600 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 active:translate-y-1px"
                        >
                            Salvar
                        </button>
                    </div>
                </form>
            </section>
        </div>
    );
}