"use client";

import { useState } from 'react'
import Sidebar from './sidebar'
import EmptyState from './emptyState'
import { ModalTask } from './modalTask'

export default function Page() {
    const [isOpen, setIsOpen] = useState(false);
    return (
        <main className="bg-white">
            <div className="w-full px-4 py-6 lg:px-8">
                <div className="grid grid-cols-1 min-h-[calc(100vh-4rem)] gap-16 lg:grid-cols-[320px_1fr]">
                    <aside className="rounded-2xl h-auto bg-[#6FA4FF] text-white">
                        <Sidebar />
                    </aside>
                    <section className="flex flex-col">
                        <div className="flex items-start justify-between">
                            <div>
                                <h1 className="text-4xl font-bold text-gray-900">Tarefas</h1>
                                <p className="mt-2 text-gray-600">Mantenha o foco! Uma tarefa de cada vez.</p>
                            </div>
                            <button
                                onClick={() => setIsOpen(true)}
                                className="mt-1 inline-flex items-center gap-2 rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:opacity-90 focus:outline-none">
                                <span className="inline-flex h-5 w-5 items-center justify-center rounded-md bg-gray-800 text-white">+</span>
                                Criar Tarefa
                            </button>
                        </div>
                        <div className="mt-8">
                            <div className="min-h-[calc(100vh-12rem)] rounded-xl border border-gray-200">
                                <div className="p-10">
                                    <EmptyState />
                                </div>
                            </div>
                        </div>
                    </section>
                </div>
            </div>
            <ModalTask open={isOpen} onClose={() => setIsOpen(false)} />
        </main>
    )
}
