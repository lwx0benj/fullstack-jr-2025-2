// components/EmptyState.tsx
import Image from 'next/image'

export default function EmptyState() {
  return (
    <div className="flex flex-col items-center gap-6 text-center">
      <p className="max-w-md text-gray-600">
        Você ainda não tem tarefas.
        <br />
        Que tal criar uma agora?
      </p>
      <div className="relative h-52 w-72">
        <Image
          src="/oversight-cuate.svg"
          alt="Ilustração de pessoa procurando tarefas"
          fill
          className="object-contain"
          priority
        />
      </div>
    </div>
  )
}
