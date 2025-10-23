// components/NavButton.tsx
import Image from 'next/image'

type Props = {
  label: string
  icon?: 'task' | 'user'
  active?: boolean
}

export default function NavButton({ label, icon = 'user', active = false }: Props) {
  const base =
    'flex items-center gap-3 rounded-xl px-4 py-3 text-left text-sm font-medium transition-colors'
  const activeCls = active ? 'bg-white text-gray-900' : 'bg-white/10 text-white hover:bg-white/20'

  return (
    <button className={[base, activeCls].join(' ')}>
      <span className="inline-flex h-5 w-5 items-center justify-center">
        <Image
          src={`/${icon}.svg`}
          alt={`${label} ícone`}
          width={20}
          height={20}
          className={active ? 'opacity-100' : 'opacity-90'}
        />
      </span>
      <span>{label}</span>
    </button>
  )
}
