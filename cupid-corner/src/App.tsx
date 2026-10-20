import { useEffect, useRef, useState, type CSSProperties, type FormEvent, type PointerEvent } from 'react'
import { useGSAP } from '@gsap/react'
import { gsap } from 'gsap'
import { ArrowDown, ArrowLeft, ArrowRight, Check, Clock3, Compass, Copy, Flower2, Gift, HandHeart, Heart, LockKeyhole, MailOpen, MessageCircle, Send, Sparkles, Sprout, Sun, UnlockKeyhole } from 'lucide-react'
import './App.css'

gsap.registerPlugin(useGSAP)

const littleThings = [
  { icon: '☼', title: 'The way you show up', text: 'Even on the days you feel a little unfinished, you bring something only you can.' },
  { icon: '✳', title: 'Your soft spots', text: 'The things you care about so much? They are not too much. They are part of your magic.' },
  { icon: '♡', title: 'All your becoming', text: 'You can change your mind, take the long way, begin again. You are allowed to be a work in progress.' },
  { icon: '✧', title: 'Your small, strange joys', text: 'The song you replay. The snack you love. The things that make you feel a little more like yourself.' },
  { icon: '☁', title: 'The care you give', text: 'A patient listen, a remembered detail, a tiny kindness. The world is softer where you are.' },
  { icon: '❋', title: 'Your wonderfully human heart', text: 'Messy, hopeful, sometimes unsure, and still willing to love. That is a pretty remarkable thing.' },
]

const notes = [
  'You make the ordinary feel a little more golden.',
  'Somewhere, someone is glad the world has you in it.',
  'You don’t have to earn your place here. You already belong.',
]

const supportOptions = [
  { id: 'confidence', icon: '✦', title: 'A confidence boost', message: 'You’re allowed to take up space. Your ideas, your laugh, your whole self belong in the room.', signoff: 'For when you need to remember your own light.' },
  { id: 'rest', icon: '☁', title: 'Permission to pause', message: 'You don’t have to turn every moment into progress. Rest is part of being a person, too.', signoff: 'A softer pace still gets you there.' },
  { id: 'belonging', icon: '♡', title: 'A reminder you matter', message: 'You matter in the quiet ways, the everyday ways, and even on the days you can’t quite feel it.', signoff: 'A little truth to keep close.' },
]

const selfLoveIdeas = [
  { icon: '“ ”', title: 'Use a kinder voice', text: 'Try speaking to yourself the way you would to someone you love.' },
  { icon: '☾', title: 'Let a pause count', text: 'You do not have to be useful every minute to deserve a breather.' },
  { icon: '✧', title: 'Notice what went right', text: 'Give yourself credit for one small thing you handled today.' },
]

const shareNotes = [
  'Just a little reminder: I’m really glad you’re in my life.',
  'You make ordinary days feel warmer. I hope you know that.',
  'No need to reply. Just sending a little love your way today.',
  'I saw something that made me think of you, and it made me smile.',
]

const loveCompassPaths = [
  {
    id: 'me', label: 'Me', icon: '♡', ideas: [
      { action: 'Take one thing off your list.', note: 'I’m allowed to make today a little gentler. I don’t have to do it all at once.' },
      { action: 'Make room for a small joy.', note: 'This little thing that makes me happy matters. I’m allowed to enjoy it.' },
      { action: 'Notice what you made it through.', note: 'I did what I could with what I had today. That counts, and so do I.' },
    ],
  },
  {
    id: 'friend', label: 'A friend', icon: '✳', ideas: [
      { action: 'Send a no-pressure check-in.', note: 'Hey, you crossed my mind today. No need to reply — just wanted you to know I’m glad you’re here.' },
      { action: 'Name one thing you appreciate.', note: 'One of my favorite things about you is how you make people feel welcome. I hope you know that.' },
      { action: 'Invite them into an ordinary moment.', note: 'Want to take a little walk or get a snack together sometime this week?' },
    ],
  },
  {
    id: 'miss', label: 'Someone I miss', icon: '☾', ideas: [
      { action: 'Share a memory that found you.', note: 'I remembered that time we laughed until we couldn’t talk. It still makes me smile. Thinking of you.' },
      { action: 'Send a small hello, with no pressure.', note: 'Just wanted to say I’m thinking of you and hope something kind finds its way into your day.' },
      { action: 'Tell them what you still carry.', note: 'A little piece of what you taught me still comes along wherever I go. I’m grateful for you.' },
    ],
  },
]

const dailyKindnessIdeas = [
  { title: 'Tell someone what you appreciate about them.', detail: 'Be specific. The small thing they do might be the thing they remember.' },
  { title: 'Send a “thinking of you” with no reply needed.', detail: 'A little warmth can travel without asking anything back.' },
  { title: 'Let yourself take a real pause.', detail: 'Put one thing down for a moment. You’re allowed to be a person, not a to-do list.' },
  { title: 'Make someone’s next minute a little easier.', detail: 'Hold the door, share the credit, or take one tiny task off their hands.' },
  { title: 'Ask someone how they are, then really listen.', detail: 'You don’t have to fix anything. Being there is already a kind thing.' },
  { title: 'Say something kind to yourself out loud.', detail: 'Try: “I’m learning, and I deserve patience while I do.”' },
  { title: 'Share a small joy with someone.', detail: 'A song, a silly photo, a good snack recommendation — joy likes company.' },
]

const gardenSeeds = [
  { id: 'self', label: 'Self-kindness', icon: Heart },
  { id: 'friendship', label: 'Friendship', icon: Sun },
  { id: 'encouragement', label: 'Encouragement', icon: Sparkles },
]

type GardenState = { count: number; blooms: { kind: string; id: number }[] }
type CareStyle = { id: string; title: string; detail: string; tryIt: string }
type CapsuleNote = { text: string; savedAt: string }

const careStyles: CareStyle[] = [
  { id: 'words', title: 'Words that stay with you', detail: 'A sincere, specific “I see you” can feel like a warm place to land.', tryIt: 'Offer yourself one kind, true sentence today. Then tell someone what you appreciate about them.' },
  { id: 'time', title: 'Time that feels like yours', detail: 'Being fully there — without rushing to fix or perform — is its own kind of gift.', tryIt: 'Make a little unhurried space for yourself or someone you love, even if it is only ten minutes.' },
  { id: 'help', title: 'Care you can feel', detail: 'Small, thoughtful help can say “you don’t have to carry this alone.”', tryIt: 'Ask what would make today easier. Remember to let someone do the same for you.' },
  { id: 'surprises', title: 'Thoughtful little surprises', detail: 'A remembered detail can say “I was listening, and I thought of you.”', tryIt: 'Send a song, bring a favorite snack, or leave yourself a tiny treat for later.' },
]

const loveQuizQuestions = [
  { prompt: 'What makes you feel most seen?', options: [
    { id: 'words', label: 'Hearing what someone appreciates about me', icon: MessageCircle },
    { id: 'time', label: 'Having someone’s full attention', icon: Clock3 },
    { id: 'help', label: 'Someone noticing what I need help with', icon: HandHeart },
    { id: 'surprises', label: 'A little surprise that shows they remembered', icon: Gift },
  ] },
  { prompt: 'How do you often show someone you care?', options: [
    { id: 'words', label: 'I say the kind thing I hope they hear', icon: MessageCircle },
    { id: 'time', label: 'I make time to be together', icon: Clock3 },
    { id: 'help', label: 'I find a practical way to help', icon: HandHeart },
    { id: 'surprises', label: 'I bring or make them a small something', icon: Gift },
  ] },
  { prompt: 'On a hard day, what would feel like care?', options: [
    { id: 'words', label: 'A reminder that I can get through this', icon: MessageCircle },
    { id: 'time', label: 'A quiet moment with someone I trust', icon: Clock3 },
    { id: 'help', label: 'One thing taken off my plate', icon: HandHeart },
    { id: 'surprises', label: 'An unexpected little comfort', icon: Gift },
  ] },
]

const rippleActions = [
  { title: 'Send a kind message', detail: 'Let someone know one specific thing you love about them.' },
  { title: 'Make a little room', detail: 'Offer your full attention for a few minutes, with no fixing required.' },
  { title: 'Lighten the load', detail: 'Ask what small thing would make today easier for someone.' },
]

const getLocalDateKey = (date: Date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const getDailyKindnessIndex = (date: Date) => {
  const dayNumber = Math.floor(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()) / 86_400_000)
  return ((dayNumber % dailyKindnessIdeas.length) + dailyKindnessIdeas.length) % dailyKindnessIdeas.length
}

const readKindnessDone = (dateKey: string) => {
  try {
    return window.localStorage.getItem(`cupids-corner-kindness:${dateKey}`) === 'done'
  } catch {
    return false
  }
}

const readGarden = (): GardenState => {
  try {
    const saved = window.localStorage.getItem('cupids-corner-garden')
    if (!saved) return { count: 0, blooms: [] }
    const parsed = JSON.parse(saved) as GardenState
    if (typeof parsed.count !== 'number' || !Array.isArray(parsed.blooms)) return { count: 0, blooms: [] }
    return { count: Math.max(0, parsed.count), blooms: parsed.blooms.slice(-9) }
  } catch {
    return { count: 0, blooms: [] }
  }
}

const readCapsuleNote = (): CapsuleNote | null => {
  try {
    const saved = window.localStorage.getItem('cupids-corner-future-note')
    if (!saved) return null
    const parsed = JSON.parse(saved) as CapsuleNote
    return typeof parsed.text === 'string' && typeof parsed.savedAt === 'string' ? parsed : null
  } catch {
    return null
  }
}

function App() {
  const page = useRef<HTMLElement>(null)
  const [today] = useState(() => new Date())
  const todayKey = getLocalDateKey(today)
  const [noteOpen, setNoteOpen] = useState(false)
  const [noteIndex, setNoteIndex] = useState(0)
  const [selectedSupport, setSelectedSupport] = useState<string | null>(null)
  const [shareNoteIndex, setShareNoteIndex] = useState(0)
  const [copyStatus, setCopyStatus] = useState<'idle' | 'copied' | 'error'>('idle')
  const [compassPathId, setCompassPathId] = useState('me')
  const [compassIdeaIndex, setCompassIdeaIndex] = useState(0)
  const [compassCopyStatus, setCompassCopyStatus] = useState<'idle' | 'copied' | 'error'>('idle')
  const [kindnessDone, setKindnessDone] = useState(() => readKindnessDone(todayKey))
  const [garden, setGarden] = useState<GardenState>(readGarden)
  const [loveQuizAnswers, setLoveQuizAnswers] = useState<string[]>([])
  const [loveQuizStep, setLoveQuizStep] = useState(0)
  const [selectedRipple, setSelectedRipple] = useState(0)
  const [rippleCount, setRippleCount] = useState(0)
  const [capsuleNote, setCapsuleNote] = useState<CapsuleNote | null>(readCapsuleNote)
  const [capsuleDraft, setCapsuleDraft] = useState('')
  const [capsuleEditing, setCapsuleEditing] = useState(false)
  const [capsuleOpen, setCapsuleOpen] = useState(false)
  const [capsuleStorageError, setCapsuleStorageError] = useState(false)
  const [game, setGame] = useState<'ready' | 'playing' | 'won' | 'lost'>('ready')
  const [caught, setCaught] = useState(0)
  const [seconds, setSeconds] = useState(12)
  const [heartSpot, setHeartSpot] = useState({ x: 50, y: 50 })
  const dailyKindness = dailyKindnessIdeas[getDailyKindnessIndex(today)]

  const plantSeed = (kind: string) => {
    const next = { count: garden.count + 1, blooms: [...garden.blooms, { kind, id: garden.count + 1 }].slice(-9) }
    setGarden(next)
    try {
      window.localStorage.setItem('cupids-corner-garden', JSON.stringify(next))
    } catch {
      // Keep the garden growing for this visit if browser storage is unavailable.
    }
  }

  const markKindnessDone = () => {
    setKindnessDone(true)
    try {
      window.localStorage.setItem(`cupids-corner-kindness:${todayKey}`, 'done')
    } catch {
      // Keep the completion for this visit if browser storage is unavailable.
    }
  }

  const recordQuizAnswer = (answer: string) => {
    setLoveQuizAnswers((answers) => {
      const next = [...answers]
      next[loveQuizStep] = answer
      return next
    })
  }

  const loveStyleResult = careStyles.reduce((best, style) => {
    const styleCount = loveQuizAnswers.filter((answer) => answer === style.id).length
    const bestCount = loveQuizAnswers.filter((answer) => answer === best.id).length
    return styleCount > bestCount ? style : best
  }, careStyles[0])

  const sealCapsuleNote = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const nextNote = { text: capsuleDraft.trim(), savedAt: new Date().toISOString() }
    setCapsuleNote(nextNote)
    setCapsuleOpen(false)
    setCapsuleEditing(false)
    try {
      window.localStorage.setItem('cupids-corner-future-note', JSON.stringify(nextNote))
      setCapsuleStorageError(false)
    } catch {
      setCapsuleStorageError(true)
    }
  }

  const writeAnotherCapsuleNote = () => {
    setCapsuleDraft(capsuleNote?.text ?? '')
    setCapsuleEditing(true)
    setCapsuleOpen(false)
  }

  useEffect(() => {
    if (game !== 'playing') return
    const timer = window.setInterval(() => setSeconds((remaining) => {
      if (remaining <= 1) { window.clearInterval(timer); setGame('lost'); return 0 }
      return remaining - 1
    }), 1000)
    return () => window.clearInterval(timer)
  }, [game])

  const startGame = () => { setCaught(0); setSeconds(12); setGame('playing') }
  const catchHeart = () => {
    const next = caught + 1
    setCaught(next)
    if (next === 3) { setGame('won'); return }
    setHeartSpot({ x: 17 + Math.random() * 66, y: 23 + Math.random() * 52 })
  }
  const selectedSupportOption = supportOptions.find((option) => option.id === selectedSupport)
  const selectedCompassPath = loveCompassPaths.find((path) => path.id === compassPathId) ?? loveCompassPaths[0]
  const compassIdea = selectedCompassPath.ideas[compassIdeaIndex]
  const chooseCompassPath = (pathId: string) => {
    setCompassPathId(pathId)
    setCompassIdeaIndex(0)
    setCompassCopyStatus('idle')
  }
  const copyCompassNote = async () => {
    try {
      await navigator.clipboard.writeText(compassIdea.note)
      setCompassCopyStatus('copied')
    } catch {
      setCompassCopyStatus('error')
    }
  }
  const copyShareNote = async () => {
    try {
      await navigator.clipboard.writeText(shareNotes[shareNoteIndex])
      setCopyStatus('copied')
    } catch {
      setCopyStatus('error')
    }
  }

  const moveHeroArt = (event: PointerEvent<HTMLElement>) => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches || window.matchMedia('(hover: none)').matches) return
    const bounds = event.currentTarget.getBoundingClientRect()
    const x = (event.clientX - bounds.left) / bounds.width - 0.5
    const y = (event.clientY - bounds.top) / bounds.height - 0.5
    gsap.to('.hero-art', { x: x * 16, y: y * 12, duration: 0.65, ease: 'power2.out', overwrite: true })
  }

  const resetHeroArt = () => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    gsap.to('.hero-art', { x: 0, y: 0, duration: 0.8, ease: 'power3.out', overwrite: true })
  }

  useGSAP(() => {
    const motionOK = !window.matchMedia('(prefers-reduced-motion: reduce)').matches
    if (!motionOK) return

    gsap.timeline({ defaults: { ease: 'power2.out' } })
      .from('.topbar', { y: -12, opacity: 0, duration: 0.55 })
      .from('.hero-copy > *, .hero-art', { y: 17, opacity: 0, duration: 0.72, stagger: 0.08 }, '-=0.22')

    gsap.to('.floating-heart', { y: -9, rotation: 5, duration: 2.2, repeat: -1, yoyo: true, ease: 'sine.inOut' })
    gsap.to('.scribble-a, .scribble-c', { rotation: '+=9', scale: 1.08, duration: 2.4, stagger: 0.4, repeat: -1, yoyo: true, ease: 'sine.inOut' })

    gsap.utils.toArray<HTMLElement>('.reason, .support-heading, .support-options, .support-card, .self-love-heading, .self-love-item, .self-love-link, .compass-heading, .compass-experience, .love-quiz-heading, .love-quiz-panel, .kindness-heading, .kindness-card, .garden-heading, .garden-experience, .ripple-heading, .ripple-panel, .share-copy, .share-card, .game-intro, .game-panel, .note-copy, .letter, .capsule-heading, .capsule-panel').forEach((element, index) => {
      gsap.from(element, {
        y: 20,
        opacity: 0,
        duration: 0.68,
        delay: index % 3 * 0.035,
        ease: 'power2.out',
        scrollTrigger: { trigger: element, start: 'top 88%', once: true },
      })
    })
  }, { scope: page })

  return (
    <main className="love-page" ref={page}>
      <header className="topbar">
        <a className="brand" href="#home" aria-label="Cupid's little corner home"><span className="brand-heart"><Heart size={17} fill="currentColor" /></span> cupid’s corner</a>
        <nav aria-label="Main navigation"><a href="#why">Why Cupid loves you</a><a href="#self-love">Love yourself</a><a href="#share">Pass it on</a></nav>
        <a className="nav-love" href="#note">For you, <Heart size={14} fill="currentColor" /></a>
      </header>

      <section className="hero" id="home" onPointerMove={moveHeroArt} onPointerLeave={resetHeroArt}>
        <div className="hero-copy">
          <p className="hello-tag"><span className="hello-dot" /> a tiny dispatch from cupid</p>
          <h1>Oh, look at<br />you. <span>Being</span><br /><span className="loved-word">lovable.</span></h1>
          <p className="hero-text">Cupid loves the big, beautiful, gloriously human thing you are. (Yes, you. Come closer.)</p>
          <a className="pill-button" href="#why">Come on in <ArrowDown size={16} /></a>
          <span className="hero-aside">A REMINDER, FOR WHEN YOU NEED ONE</span>
        </div>
        <div className="hero-art" aria-label="A cheerful illustration of a heart surrounded by flowers and stars">
          <div className="sun-disc" />
          <span className="scribble scribble-a">✳</span><span className="scribble scribble-b">✷</span><span className="scribble scribble-c">✦</span>
          <span className="tiny-heart heart-a">♡</span><span className="tiny-heart heart-b">♡</span>
          <div className="flower flower-a"><i /><b /><em /><strong /></div>
          <div className="flower flower-b"><i /><b /><em /><strong /></div>
          <div className="flower flower-c"><i /><b /><em /><strong /></div>
          <div className="hero-heart floating-heart"><Heart size={136} strokeWidth={1.15} fill="currentColor" /></div>
          <div className="orbit-note">made of<br />the good stuff</div>
          <span className="art-caption">a perfectly imperfect heart</span>
        </div>
        <span className="hero-index">№ 001 <i>♡</i> KEEP THIS CLOSE</span>
      </section>

      <section className="why" id="why">
        <div className="why-heading"><p className="section-note">Cupid has been paying attention</p><h2>So many reasons<br />to love <span>people like you.</span></h2></div>
        <div className="reason-list">
          {littleThings.map((item, index) => <article className={`reason reason-${index + 1}`} key={item.title}>
            <span className="reason-symbol" aria-hidden="true">{item.icon}</span>
            <div><h3>{item.title}</h3><p>{item.text}</p></div>
            <span className="reason-heart" aria-hidden="true">♡</span>
          </article>)}
        </div>
        <p className="why-footnote">No checklist, no perfect version required. Just you.</p>
      </section>

      <section className="support-section" id="support" aria-labelledby="support-title">
        <div className="support-heading"><p className="section-note">A small check-in with yourself</p><h2 id="support-title">What would feel<br />good <em>right now?</em></h2><p>Pick what you need. There’s no wrong answer.</p></div>
        <div className="support-experience">
          <div className="support-options" role="group" aria-label="Choose the kind of reminder you need">
            {supportOptions.map((option) => <button className={`support-option ${selectedSupport === option.id ? 'is-selected' : ''}`} key={option.id} onClick={() => setSelectedSupport(option.id)} aria-pressed={selectedSupport === option.id}>
              <span className="support-option-icon" aria-hidden="true">{option.icon}</span><span>{option.title}</span><ArrowRight size={14} />
            </button>)}
          </div>
          <div className="support-card" key={selectedSupportOption?.id ?? 'default'} aria-live="polite" aria-atomic="true">
            <span className="support-card-heart"><Heart size={21} fill="currentColor" /></span>
            <p className="support-card-label">{selectedSupportOption ? 'A LITTLE REMINDER FOR YOU' : 'CUPID’S POCKET OF KINDNESS'}</p>
            <p className="support-message">{selectedSupportOption ? selectedSupportOption.message : 'Choose a feeling on the left. Cupid packed a few gentle words for the moment you’re in.'}</p>
            <p className="support-signoff">{selectedSupportOption ? selectedSupportOption.signoff : 'A little care, whenever you need it.'}</p>
          </div>
        </div>
      </section>

      <section className="self-love-section" id="self-love" aria-labelledby="self-love-title">
        <div className="self-love-heading"><span className="self-love-orbit" aria-hidden="true"><Heart size={26} fill="currentColor" /></span><p className="section-note">Cupid’s gentle reminder</p><h2 id="self-love-title">Save a little<br />love <em>for yourself.</em></h2><p>You belong in the circle of care you give everyone else.</p></div>
        <div className="self-love-list">
          {selfLoveIdeas.map((idea, index) => <article className={`self-love-item self-love-item-${index + 1}`} key={idea.title}><span className="self-love-symbol" aria-hidden="true">{idea.icon}</span><div><h3>{idea.title}</h3><p>{idea.text}</p></div></article>)}
          <a className="self-love-link" href="#support">Find the words you need <ArrowRight size={15} /></a>
        </div>
      </section>

      <section className="interlude"><Sparkles size={19} /><p>Love is not a candle.<br />Lighting someone else’s <em>doesn’t dim yours.</em></p><span>THERE IS ROOM FOR ALL OF US.</span></section>

      <section className="compass-section" id="compass" aria-labelledby="compass-title">
        <div className="compass-heading">
          <span className="compass-mark" aria-hidden="true"><Compass size={23} /></span>
          <p className="section-note">A little love, pointed somewhere</p>
          <h2 id="compass-title">Where could your<br />love <em>land today?</em></h2>
          <p>Pick a direction. Cupid will help with one small, real way to show you care.</p>
        </div>
        <div className="compass-experience">
          <div className="compass-choices" role="group" aria-label="Who would you like to show love to?">
            {loveCompassPaths.map((path) => <button className={`compass-choice ${compassPathId === path.id ? 'is-selected' : ''}`} key={path.id} onClick={() => chooseCompassPath(path.id)} aria-pressed={compassPathId === path.id}>
              <span aria-hidden="true">{path.icon}</span>{path.label}
            </button>)}
          </div>
          <div className="compass-result" aria-live="polite" aria-atomic="true">
            <p className="compass-result-label"><span /> YOUR NEXT KIND THING</p>
            <h3 key={`${compassPathId}-${compassIdeaIndex}`}>{compassIdea.action}</h3>
            <div className="compass-note"><Heart size={16} fill="currentColor" /><p>{compassIdea.note}</p></div>
            <div className="compass-actions">
              <button className="compass-another" onClick={() => { setCompassIdeaIndex((index) => (index + 1) % selectedCompassPath.ideas.length); setCompassCopyStatus('idle') }}>Another idea <ArrowRight size={14} /></button>
              <button className="compass-copy" onClick={copyCompassNote}>{compassCopyStatus === 'copied' ? <Check size={15} /> : <Copy size={15} />}{compassCopyStatus === 'copied' ? 'Copied' : 'Copy note'}</button>
            </div>
            <p className={`compass-feedback ${compassCopyStatus}`} aria-live="polite">{compassCopyStatus === 'copied' ? 'Ready to send, or make it sound like you.' : compassCopyStatus === 'error' ? 'Copy is unavailable here. Select the note above to copy it.' : 'A starting point, in your own words.'}</p>
          </div>
        </div>
      </section>

      <section className="love-quiz-section" id="love-quiz" aria-labelledby="love-quiz-title">
        <div className="love-quiz-heading">
          <p className="section-note">A tiny bit of self-discovery</p>
          <h2 id="love-quiz-title">How does love<br />feel like <em>you?</em></h2>
          <p>Three little questions to notice the ways care reaches you — and the ways you already give it.</p>
        </div>
        <div className="love-quiz-panel">
          <div className="love-quiz-progress">
            <span>{loveQuizStep < loveQuizQuestions.length ? `QUESTION ${loveQuizStep + 1} OF ${loveQuizQuestions.length}` : 'YOUR LOVE SIGNAL'}</span>
            <div role="progressbar" aria-label="Quiz progress" aria-valuemin={0} aria-valuemax={loveQuizQuestions.length} aria-valuenow={Math.min(loveQuizStep + 1, loveQuizQuestions.length)}><span style={{ width: `${Math.min(((loveQuizStep + 1) / loveQuizQuestions.length) * 100, 100)}%` }} /></div>
          </div>
          {loveQuizStep < loveQuizQuestions.length ? <>
            <h3 className="love-quiz-question" key={loveQuizStep}>{loveQuizQuestions[loveQuizStep].prompt}</h3>
            <div className="love-quiz-options" role="group" aria-label="Choose the answer that feels most like you">
              {loveQuizQuestions[loveQuizStep].options.map((option) => { const OptionIcon = option.icon; return <button className={`love-quiz-option ${loveQuizAnswers[loveQuizStep] === option.id ? 'is-selected' : ''}`} key={option.id} onClick={() => recordQuizAnswer(option.id)} aria-pressed={loveQuizAnswers[loveQuizStep] === option.id}><OptionIcon size={17} /><span>{option.label}</span><span className="quiz-option-check">{loveQuizAnswers[loveQuizStep] === option.id ? <Check size={14} /> : null}</span></button> })}
            </div>
            <div className="love-quiz-controls">
              <button className="quiz-back" onClick={() => setLoveQuizStep((step) => Math.max(0, step - 1))} disabled={loveQuizStep === 0}><ArrowLeft size={14} /> Back</button>
              <button className="quiz-next" onClick={() => setLoveQuizStep((step) => step + 1)} disabled={!loveQuizAnswers[loveQuizStep]}>{loveQuizStep === loveQuizQuestions.length - 1 ? 'Find my love signal' : 'Next question'} <ArrowRight size={14} /></button>
            </div>
          </> : <div className="love-quiz-result" aria-live="polite">
            <span className="quiz-result-heart"><Heart size={19} fill="currentColor" /></span>
            <p className="quiz-result-label">YOUR CARE COMES THROUGH IN</p>
            <h3>{loveStyleResult.title}</h3>
            <p>{loveStyleResult.detail}</p>
            <div className="quiz-result-try"><Sparkles size={15} /><span>{loveStyleResult.tryIt}</span></div>
            <button className="quiz-restart" onClick={() => { setLoveQuizAnswers([]); setLoveQuizStep(0) }}>Take the little quiz again <ArrowRight size={14} /></button>
          </div>}
        </div>
      </section>

      <section className="kindness-section" aria-labelledby="kindness-title">
        <div className="kindness-heading">
          <p className="section-note">A fresh little nudge each day</p>
          <h2 id="kindness-title">Today’s kindness<br />can be <em>small.</em></h2>
          <p>No grand gestures needed. Just one thoughtful thing, for you or someone else.</p>
        </div>
        <div className={`kindness-card ${kindnessDone ? 'is-done' : ''}`}>
          <div className="kindness-date"><Sparkles size={15} /><time dateTime={todayKey}>{today.toLocaleDateString(undefined, { weekday: 'long', month: 'long', day: 'numeric' })}</time></div>
          <h3>{dailyKindness.title}</h3>
          <p className="kindness-detail">{dailyKindness.detail}</p>
          <button className="kindness-button" onClick={markKindnessDone} disabled={kindnessDone}>
            {kindnessDone ? <><Check size={15} /> A little kindness is out in the world</> : <>I did this little thing <Heart size={14} /></>}
          </button>
          <p className="kindness-footnote" aria-live="polite">{kindnessDone ? 'Lovely. Your reminder will be here tomorrow.' : 'One small thing is more than enough.'}</p>
        </div>
      </section>

      <section className="garden-section" id="love-garden" aria-labelledby="garden-title">
        <div className="garden-heading">
          <p className="section-note">A little patch of good</p>
          <h2 id="garden-title">Kindness grows<br />when we <em>tend it.</em></h2>
          <p>Plant a small intention for yourself or someone else. Every kind thought gets a place to bloom.</p>
        </div>
        <div className="garden-experience">
          <div className="garden-topline"><span>YOUR LOVE GARDEN</span><span aria-live="polite">{garden.count} {garden.count === 1 ? 'little bloom' : 'little blooms'}</span></div>
          <div className={`garden-meadow ${garden.blooms.length ? 'has-blooms' : ''}`} role="img" aria-label={garden.count ? `A small garden with ${garden.count} planted intentions` : 'An empty little garden, ready for its first seed'}>
            {garden.blooms.length ? garden.blooms.map((bloom, index) => <span className={`garden-bloom bloom-${bloom.kind}`} key={bloom.id} style={{ '--bloom-delay': `${index * 40}ms` } as CSSProperties} aria-hidden="true"><Flower2 size={27 + (index % 3) * 5} strokeWidth={1.5} /></span>) : <p className="garden-empty"><Sprout size={17} />Plant a first little seed</p>}
            <span className="garden-ground" />
          </div>
          <p className="garden-prompt">Choose a seed to plant</p>
          <div className="garden-seeds" role="group" aria-label="Choose what kind of kindness to plant">
            {gardenSeeds.map(({ id, label, icon: SeedIcon }) => <button className="garden-seed" key={id} onClick={() => plantSeed(id)} aria-label={`Plant ${id === 'encouragement' ? 'an' : 'a'} ${label.toLowerCase()} seed`}><SeedIcon size={16} /><span>{label}</span><span className="garden-plus" aria-hidden="true">+</span></button>)}
          </div>
          <p className="garden-footnote">Your garden stays right here in this browser.</p>
        </div>
      </section>

      <section className="ripple-section" id="love-ripple" aria-labelledby="ripple-title">
        <div className="ripple-heading">
          <p className="section-note">Little things keep travelling</p>
          <h2 id="ripple-title">Start a love<br /><em>ripple.</em></h2>
          <p>Pick one small act of care. Imagine where its warmth could go next.</p>
          <div className="ripple-actions" role="group" aria-label="Choose a kind action">
            {rippleActions.map((action, index) => <button className={`ripple-action ${selectedRipple === index ? 'is-selected' : ''}`} key={action.title} onClick={() => setSelectedRipple(index)} aria-pressed={selectedRipple === index}><span>{String(index + 1).padStart(2, '0')}</span>{action.title}</button>)}
          </div>
          <p className="ripple-action-detail" aria-live="polite">{rippleActions[selectedRipple].detail}</p>
        </div>
        <div className="ripple-panel">
          <div className="ripple-scene" key={rippleCount || 'still'} aria-hidden="true">
            {rippleCount > 0 && <><span className="ripple-ring ring-one" /><span className="ripple-ring ring-two" /><span className="ripple-ring ring-three" /></>}
            <span className="ripple-center"><Heart size={24} fill="currentColor" /></span>
          </div>
          <p className="ripple-caption" aria-live="polite">{rippleCount ? 'A little kindness is on its way.' : 'A small act can start right here.'}</p>
          <ol className={`ripple-chain ${rippleCount ? 'is-flowing' : ''}`}>
            <li>Someone may feel a little more seen</li>
            <li>They might pass along some patience</li>
            <li>A moment gets softer somewhere nearby</li>
          </ol>
          <button className="ripple-send" onClick={() => setRippleCount((count) => count + 1)}>Send this little ripple <Send size={15} /></button>
        </div>
      </section>

      <section className="share-section" id="share" aria-labelledby="share-title">
        <div className="share-copy"><p className="section-note">A little love goes a long way</p><h2 id="share-title">Pass the good<br />feeling <em>along.</em></h2><p>A check-in. A kind word. A note that says “you crossed my mind.” Small things can make someone feel less alone.</p><div className="share-ideas"><span><i>01</i> Tell someone what you appreciate about them.</span><span><i>02</i> Send a no-pressure “thinking of you.”</span><span><i>03</i> Include yourself in the kindness, too.</span></div></div>
        <div className="share-card">
          <div className="share-card-top"><span className="share-stamp"><Heart size={16} fill="currentColor" /></span><span>YOUR POCKET-SIZED LOVE NOTE</span></div>
          <p className="share-message" key={shareNoteIndex} aria-live="polite" aria-atomic="true">{shareNotes[shareNoteIndex]}</p>
          <div className="share-actions"><button className="share-refresh" onClick={() => { setShareNoteIndex((index) => (index + 1) % shareNotes.length); setCopyStatus('idle') }}>Another little note <Sparkles size={14} /></button><button className="share-copy" onClick={copyShareNote}>{copyStatus === 'copied' ? <Check size={15} /> : <Copy size={15} />}{copyStatus === 'copied' ? 'Copied' : 'Copy note'}</button></div>
          <p className={`copy-feedback ${copyStatus}`} aria-live="polite">{copyStatus === 'copied' ? 'Ready to send to someone you love.' : copyStatus === 'error' ? 'Copy wasn’t available. You can select and copy the note above.' : 'Take it as is, or make it sound like you.'}</p>
        </div>
      </section>

      <section className="game-section" aria-labelledby="game-title">
        <div className="game-intro"><span className="game-icon"><Sparkles size={18} /></span><p className="section-note">A tiny game, just because</p><h2 id="game-title">Cupid’s heart<br />got loose.</h2><p>Catch three before it flutters away.<br />You’ve got twelve seconds. Ready?</p></div>
        <div className="game-panel">
          <div className="game-topline"><span>THE HEART HUNT</span><span className="game-count">{caught}<i>/</i>3</span></div>
          <div className={`game-arena ${game === 'playing' ? 'is-playing' : ''}`}>
            <span className="arena-spark spark-one">✦</span><span className="arena-spark spark-two">✳</span>
          {game === 'playing' ? <button className="catch-heart" key={caught} style={{ left: `${heartSpot.x}%`, top: `${heartSpot.y}%` }} onClick={catchHeart} aria-label="Catch Cupid's heart"><Heart size={37} fill="currentColor" /></button> : <div className="arena-message"><span className="arena-heart"><Heart size={29} fill="currentColor" /></span><p>{game === 'won' ? 'You caught it! Keep that love.' : game === 'lost' ? 'It fluttered off. Try once more?' : 'A tiny love is hiding in here.'}</p></div>}
          </div>
          <div className="game-controls"><span className="game-time" aria-live="polite">{game === 'playing' ? `00:${String(seconds).padStart(2, '0')}` : game === 'won' ? 'Lovely!' : '12 seconds'}</span><button className="game-button" onClick={game === 'playing' ? undefined : startGame} disabled={game === 'playing'}>{game === 'playing' ? 'Catch the heart' : game === 'won' || game === 'lost' ? 'Play again' : 'Let’s play'} <ArrowRight size={14} /></button></div>
        </div>
      </section>

      <section className="note-section" id="note">
        <div className="note-copy"><p className="section-note">Pssst. This one’s yours.</p><h2>Something small<br />to keep <em>near.</em></h2><p>For the loud days, the quiet ones, and every in-between.</p>
          <button className="note-button" onClick={() => { setNoteOpen((open) => !open); if (noteOpen) setNoteIndex((index) => (index + 1) % notes.length) }} aria-expanded={noteOpen} aria-controls="love-letter">
            <MailOpen size={16} /> {noteOpen ? 'Another little note' : 'Open your little note'} <ArrowRight size={15} />
          </button>
        </div>
        <div className={`letter ${noteOpen ? 'letter-open' : ''}`} id="love-letter" aria-live="polite">
          <div className="letter-stamp"><Heart size={18} fill="currentColor" /></div>
          <p className="letter-from">A NOTE FROM CUPID</p>
          <p className="letter-greeting">Hey, you.</p>
          <p className="letter-body">{noteOpen ? notes[noteIndex] : 'There’s a little something waiting inside…'}</p>
          <p className="letter-signoff">With a whole lot of love,<br /><span>cupid <Heart size={15} fill="currentColor" /></span></p>
          {!noteOpen && <div className="letter-seal"><Heart size={18} fill="currentColor" /></div>}
        </div>
      </section>

      <section className="capsule-section" id="future-note" aria-labelledby="capsule-title">
        <div className="capsule-heading">
          <p className="section-note">A little kindness, from you to you</p>
          <h2 id="capsule-title">Leave future-you<br />a little <em>love.</em></h2>
          <p>Write a note for another day. It stays private in this browser, ready whenever you want to open it.</p>
        </div>
        <div className={`capsule-panel ${capsuleOpen ? 'is-open' : ''}`}>
          {!capsuleNote || capsuleEditing ? <form className="capsule-form" onSubmit={sealCapsuleNote}>
            <label htmlFor="future-note-text">What would you like to remember?</label>
            <textarea id="future-note-text" value={capsuleDraft} maxLength={240} onChange={(event) => setCapsuleDraft(event.target.value)} placeholder="You’re allowed to take this one small step at a time…" rows={4} required />
            <div className="capsule-form-bottom"><span>{capsuleDraft.length}/240</span><button type="submit" className="capsule-button" disabled={!capsuleDraft.trim()}><LockKeyhole size={15} /> Seal my note</button></div>
            {capsuleEditing && <button type="button" className="capsule-cancel" onClick={() => { setCapsuleEditing(false); setCapsuleDraft('') }}>Keep the note I already wrote</button>}
          </form> : <div className="capsule-envelope">
            <span className="capsule-stamp" aria-hidden="true">{capsuleOpen ? <UnlockKeyhole size={18} /> : <LockKeyhole size={18} />}</span>
            <p className="capsule-date">SEALED {new Date(capsuleNote.savedAt).toLocaleDateString(undefined, { month: 'long', day: 'numeric', year: 'numeric' })}</p>
            {capsuleOpen ? <>
              <p className="capsule-letter" aria-live="polite">{capsuleNote.text}</p>
              <button className="capsule-button" onClick={() => setCapsuleOpen(false)}><LockKeyhole size={15} /> Tuck it away</button>
            </> : <>
              <h3>A little reminder is waiting.</h3>
              <p className="capsule-private">Only you can open this note here.</p>
              <button className="capsule-button" onClick={() => setCapsuleOpen(true)}><UnlockKeyhole size={15} /> Open my note</button>
            </>}
            <button className="capsule-cancel" onClick={writeAnotherCapsuleNote}>Write a new note</button>
            {capsuleStorageError && <p className="capsule-storage-error" role="status">This note is saved for this visit, but browser storage wasn’t available.</p>}
          </div>}
        </div>
      </section>

      <footer className="footer"><a className="brand" href="#home"><span className="brand-heart"><Heart size={15} fill="currentColor" /></span> cupid’s corner</a><p>Be gentle with yourself out there.</p><a href="#home" aria-label="Back to the top">BACK TO YOU <ArrowRight size={14} /></a></footer>
    </main>
  )
}

export default App
