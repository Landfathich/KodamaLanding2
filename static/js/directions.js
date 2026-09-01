const floatingEmojis = document.querySelectorAll('.floating-emoji');

const emojiSets = {
    'emoji-1': ['🚀', '⭐', '🔥', '💡'],
    'emoji-2': ['💻', '⌨️', '🖥️', '📱'],
    'emoji-3': ['🎮', '🕹️', '👾', '🎲'],
    'emoji-4': ['🎨', '🖌️', '✨', '🌈']
};

floatingEmojis.forEach((el, index) => {
    const emojiClass = el.classList[1];
    const emojiList = emojiSets[emojiClass];
    let currentIndex = 0;

    setInterval(() => {
        el.style.opacity = '0';
        el.style.transform = 'scale(0.5)';

        setTimeout(() => {
            currentIndex = (currentIndex + 1) % emojiList.length;
            el.textContent = emojiList[currentIndex];
            el.style.opacity = '1';
            el.style.transform = 'scale(1)';
        }, 300);
    }, 3000 + index * 500);
});