// Custom Icon Library for Kai Whiteboard
// Replaces emojis with SVG icons

const KAI_ICONS = {
    // Weather icons
    sun: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>`,
    
    cloud: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/></svg>`,
    
    rain: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 13v5M8 13v5M12 15v5M20 16.58A5 5 0 0 0 18 7h-1.26A8 8 0 1 0 4 15.25"/></svg>`,
    
    snow: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 17.58A5 5 0 0 0 18 8h-1.26A8 8 0 1 0 4 16.25M8 16h.01M8 20h.01M12 18h.01M12 22h.01M16 16h.01M16 20h.01"/></svg>`,
    
    // Action icons
    plus: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg>`,
    
    microphone: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2M12 19v4"/></svg>`,
    
    megaphone: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 11l18-5v12L3 14v-3zM11.6 16.8a3 3 0 1 1-5.8-1.6"/></svg>`,
    
    globe: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>`,
    
    surprise: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="9" r="2"/><path d="M12 15v.01"/></svg>`,
    
    // Status icons
    check: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 6L9 17l-5-5"/></svg>`,
    
    x: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>`,
    
    clock: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>`,
    
    calendar: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>`,
    
    book: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>`,
    
    moon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`,
    
    list: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>`,
    
    // Theme-specific decorative icons
    shamrock: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C10 2 8 3.5 8 5.5c0 1.5 1 2.8 2.5 3.2-.5.3-1 .8-1.2 1.4-.2.6-.1 1.3.2 1.8-.6.1-1.2.4-1.6.9-.4.5-.6 1.1-.5 1.7.1.6.4 1.2.9 1.6.5.4 1.1.6 1.7.5.3-.1.6-.2.8-.4-.1.7.1 1.4.5 1.9.4.5 1 .8 1.7.8s1.3-.3 1.7-.8c.4-.5.6-1.2.5-1.9.3.2.5.3.8.4.6.1 1.2-.1 1.7-.5.5-.4.8-1 .9-1.6.1-.6-.1-1.2-.5-1.7-.4-.5-1-.8-1.6-.9.3-.5.4-1.2.2-1.8-.2-.6-.7-1.1-1.2-1.4C17 8.3 18 7 18 5.5c0-2-2-3.5-4-3.5-1 0-1.5.5-2 1-.5-.5-1-1-2-1z"/></svg>`,
    
    dancer: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a2 2 0 1 1 0 4 2 2 0 0 1 0-4zm4 5h-4l-2 4 3 2-2 8h2l2-5 2 5h2l-2-8 3-2-2-4z"/></svg>`,
    
    temple: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 22h16M6 18v4M10 18v4M14 18v4M18 18v4M2 18h20l-10-8-10 8zM12 10V2l6 4-6 4z"/><path d="M12 2L6 6l6 4V2z"/></svg>`,
    
    pumpkin: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 3c-4 0-7 3-7 7 0 2 1 4 2 5-1 1-2 3-2 5 0 3 2 5 4 5 1 0 2-.5 3-1 1 .5 2 1 3 1 2 0 4-2 4-5 0-2-1-4-2-5 1-1 2-3 2-5 0-4-3-7-7-7z"/><circle cx="9" cy="11" r="1" fill="#000"/><circle cx="15" cy="11" r="1" fill="#000"/><path d="M8 15c1 1 3 1 4 0 1 1 3 1 4 0" stroke="#000" stroke-width="1" fill="none"/></svg>`,
    
    christmasTree: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2L2 22h20L12 2zm0 4l6 12H6l6-12z"/><rect x="11" y="18" width="2" height="4"/></svg>`,
    
    robot: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="8" cy="7" r="1" fill="currentColor"/><circle cx="16" cy="7" r="1" fill="currentColor"/><path d="M12 2v6M8 2v6M16 2v6M9 16h6"/></svg>`,
    
    // Navigation
    chevronLeft: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>`,
    
    chevronRight: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>`,
    
    // Weather conditions
    thermometer: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/></svg>`,
    
    wind: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2m15.73-8.27A2.5 2.5 0 1 1 19.5 12H2"/></svg>`,
    
    droplet: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>`
};

// Theme decoration configurations with SVG icons instead of emojis
const THEME_DECORATIONS = {
    ireland: {
        icons: ['shamrock', 'shamrock', 'shamrock'],
        colors: ['#10b981', '#059669', '#047857'],
        floating: [
            { icon: 'shamrock', top: '15%', left: '8%', delay: '0s', size: '2rem' },
            { icon: 'shamrock', top: '60%', left: '5%', delay: '1s', size: '2rem' },
            { icon: 'shamrock', top: '25%', right: '10%', delay: '2s', size: '2rem' },
        ],
        drifting: [
            { icon: 'cloud', top: '40%', delay: '0s', size: '2.5rem', opacity: 0.6 },
            { icon: 'rain', top: '70%', delay: '5s', size: '2.5rem', opacity: 0.4 },
        ]
    },
    spain: {
        icons: ['dancer', 'dancer'],
        colors: ['#dc2626', '#fbbf24', '#dc2626'],
        floating: [
            { icon: 'sun', top: '20%', left: '15%', delay: '0s', size: '2rem' },
            { icon: 'dancer', bottom: '30%', left: '10%', delay: '0s', size: '3rem' },
            { icon: 'dancer', bottom: '20%', right: '15%', delay: '0.5s', size: '3rem' },
        ],
        drifting: [
            { icon: 'sun', top: '35%', delay: '2s', size: '2.5rem', opacity: 0.6 },
        ]
    },
    thailand: {
        icons: ['temple', 'temple'],
        colors: ['#2563eb', '#fbbf24', '#dc2626'],
        floating: [
            { icon: 'temple', top: '10%', left: '12%', delay: '0s', size: '2rem' },
            { icon: 'sun', top: '45%', left: '5%', delay: '1.2s', size: '2rem' },
            { icon: 'temple', top: '30%', right: '12%', delay: '2s', size: '2rem' },
        ],
        drifting: [
            { icon: 'cloud', top: '55%', delay: '3s', size: '2.5rem', opacity: 0.5 },
        ]
    },
    halloween: {
        icons: ['pumpkin', 'moon'],
        colors: ['#ea580c', '#a855f7', '#84cc16'],
        floating: [
            { icon: 'pumpkin', top: '12%', left: '10%', delay: '0s', size: '2rem' },
            { icon: 'moon', top: '55%', left: '6%', delay: '1s', size: '2rem' },
            { icon: 'pumpkin', top: '20%', right: '10%', delay: '2s', size: '2rem' },
        ],
        falling: [
            { icon: 'cloud', left: '20%', delay: '0s', size: '2rem' },
            { icon: 'rain', left: '60%', delay: '3s', size: '2rem' },
            { icon: 'moon', left: '80%', delay: '6s', size: '2rem' },
        ]
    },
    christmas: {
        icons: ['christmasTree', 'snow'],
        colors: ['#dc2626', '#22c55e', '#fbbf24'],
        falling: [
            { icon: 'snow', left: '10%', delay: '0s', size: '1.5rem' },
            { icon: 'snow', left: '30%', delay: '2s', size: '1.5rem' },
            { icon: 'snow', left: '50%', delay: '4s', size: '1.5rem' },
            { icon: 'snow', left: '70%', delay: '1s', size: '1.5rem' },
            { icon: 'snow', left: '85%', delay: '3s', size: '1.5rem' },
        ],
        floating: [
            { icon: 'christmasTree', top: '15%', left: '15%', delay: '0s', size: '2rem' },
            { icon: 'christmasTree', top: '50%', right: '10%', delay: '1s', size: '2rem' },
        ]
    },
    ailand: {
        icons: ['robot', 'circuit'],
        colors: ['#0891b2', '#22d3ee', '#a855f7'],
        floating: [
            { icon: 'robot', top: '15%', left: '10%', delay: '0s', size: '2rem' },
            { icon: 'robot', top: '40%', left: '5%', delay: '1s', size: '2rem' },
            { icon: 'robot', top: '25%', right: '12%', delay: '2s', size: '2rem' },
        ],
        drifting: [
            { icon: 'cloud', top: '55%', delay: '3s', size: '2.5rem', opacity: 0.4 },
        ]
    }
};

// Country flag colors (as SVG circles instead of emojis)
const COUNTRY_FLAGS = {
    ireland: { colors: ['#22c55e', '#ffffff', '#f97316'], label: 'Ireland' },
    spain: { colors: ['#dc2626', '#fbbf24', '#dc2626'], label: 'Spain' },
    thailand: { colors: ['#dc2626', '#ffffff', '#2563eb'], label: 'Thailand' }
};

// Helper function to render icon
function renderIcon(iconName, size = '1.5rem', color = 'currentColor') {
    const svg = KAI_ICONS[iconName] || KAI_ICONS.sun;
    return svg.replace('stroke="currentColor"', `stroke="${color}"`)
              .replace('fill="currentColor"', `fill="${color}"`)
              .replace('width="24"', `width="${size}"`)
              .replace('height="24"', `height="${size}"`);
}

// Export for use in Vue app
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { KAI_ICONS, THEME_DECORATIONS, COUNTRY_FLAGS, renderIcon };
}
