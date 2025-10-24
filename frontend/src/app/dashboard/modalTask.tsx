"use client";

import * as React from "react";
import { Dialog } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";

type Priority = "baixa" | "media" | "alta";
type Status = "pendente" | "concluida";

export type TaskFormData = {
    titulo: string;
    prioridade: Priority;
    status: Status;
    prazo?: string;
    descricao?: string;
};

type ModalTaskProps = {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    onSave?: (data: TaskFormData) => void;
};

export function ModalTask({ open, onOpenChange, onSave }: ModalTaskProps) {
    const [form, setForm] = React.useState<TaskFormData>({
        titulo: "",
        prioridade: "media",
        status: "pendente",
        prazo: "",
        descricao: "",
    });

    function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();
        onSave?.(form);
        setForm({
            titulo: "",
            prioridade: "media",
            status: "pendente",
            prazo: "",
            descricao: "",
        })
        onOpenChange(false);
    }

    if (!open) return null; 

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            {/* Overlay */}
            <div
                className="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm"
                onClick={(e) => {
                    if (e.target === e.currentTarget) onOpenChange(false);
                }}
            />

            {/* Modal */}
            <div className="fixed inset-0 z-50 grid place-items-center p-4 sm:p-6">
                <div className="w-full max-w-[560px] rounded-2xl bg-white border border-blue-100 shadow-lg p-6 text-blue-900">
                    {/* Header */}
                    <div className="mb-4">
                        <h2
                            id="task-dialog-title"
                            className="text-xl font-bold text-blue-700"
                        >
                            Nova Tarefa
                        </h2>
                        <p className="text-blue-500">
                            Preencha os campos abaixo e clique em <b>Salvar</b>.
                        </p>
                    </div>

                    {/* Formulário */}
                    <form className="grid gap-5" onSubmit={handleSubmit}>
                        {/* Título */}
                        <div className="grid gap-2">
                            <Label htmlFor="titulo" className="text-blue-900 font-medium">
                                Título
                            </Label>
                            <Input
                                id="titulo"
                                name="titulo"
                                required
                                placeholder="Ex.: Preparar apresentação"
                                className="bg-blue-50 border-blue-200 text-blue-900 placeholder:text-blue-300 focus:ring-2 focus:ring-blue-300"
                                value={form.titulo}
                                onChange={(e) =>
                                    setForm((f) => ({ ...f, titulo: e.target.value }))
                                }
                            />
                        </div>

                        {/* Prioridade e Status */}
                        <div className="grid gap-4 sm:grid-cols-2">
                            <div className="grid gap-2">
                                <Label className="text-blue-900 font-medium">Prioridade</Label>
                                <Select
                                    value={form.prioridade}
                                    onValueChange={(v: Priority) =>
                                        setForm((f) => ({ ...f, prioridade: v }))
                                    }
                                >
                                    <SelectTrigger className="bg-blue-50 border-blue-200 text-blue-900 focus:ring-2 focus:ring-blue-300">
                                        <SelectValue placeholder="Selecione" />
                                    </SelectTrigger>
                                    <SelectContent className="bg-white text-blue-900 border-blue-200">
                                        <SelectItem value="baixa">Baixa</SelectItem>
                                        <SelectItem value="media">Média</SelectItem>
                                        <SelectItem value="alta">Alta</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>

                            <div className="grid gap-2">
                                <Label className="text-blue-900 font-medium">Status</Label>
                                <Select
                                    value={form.status}
                                    onValueChange={(v: Status) =>
                                        setForm((f) => ({ ...f, status: v }))
                                    }
                                >
                                    <SelectTrigger className="bg-blue-50 border-blue-200 text-blue-900 focus:ring-2 focus:ring-blue-300">
                                        <SelectValue placeholder="Selecione" />
                                    </SelectTrigger>
                                    <SelectContent className="bg-white text-blue-900 border-blue-200">
                                        <SelectItem value="pendente">Pendente</SelectItem>
                                        <SelectItem value="concluida">Concluída</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>
                        </div>

                        {/* Prazo */}
                        <div className="grid gap-2">
                            <Label htmlFor="prazo" className="text-blue-900 font-medium">
                                Prazo
                            </Label>
                            <Input
                                id="prazo"
                                name="prazo"
                                type="date"
                                className="bg-blue-50 border-blue-200 text-blue-900 focus:ring-2 focus:ring-blue-300"
                                value={form.prazo}
                                onChange={(e) =>
                                    setForm((f) => ({ ...f, prazo: e.target.value }))
                                }
                            />
                        </div>

                        {/* Descrição */}
                        <div className="grid gap-2">
                            <Label htmlFor="descricao" className="text-blue-900 font-medium">
                                Descrição
                            </Label>
                            <Textarea
                                id="descricao"
                                name="descricao"
                                placeholder="Detalhes, critérios de aceite, links, etc."
                                className="min-h-[120px] bg-blue-50 border-blue-200 text-blue-900 placeholder:text-blue-300 focus:ring-2 focus:ring-blue-300"
                                value={form.descricao}
                                onChange={(e) =>
                                    setForm((f) => ({ ...f, descricao: e.target.value }))
                                }
                            />
                        </div>

                        {/* Footer */}
                        <div className="mt-4 flex justify-end gap-3">
                            <Button
                                type="button"
                                variant="outline"
                                className="border-blue-300 text-blue-700 hover:bg-blue-100"
                                onClick={() => onOpenChange(false)}
                            >
                                Cancelar
                            </Button>
                            <Button
                                type="submit"
                                className="bg-blue-500 hover:bg-blue-600 text-white"
                            >
                                Salvar
                            </Button>
                        </div>
                    </form>
                </div>
            </div>
        </Dialog>
    );
}
