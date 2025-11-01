/**
 * Copy Button Functionality for Code Blocks
 * ==========================================
 * Automatically adds copy buttons to all code blocks in the page
 * with a smooth user experience and visual feedback.
 */

document.addEventListener('DOMContentLoaded', function() {
    addCopyButtons();
});

/**
 * Add copy buttons to all code blocks
 */
function addCopyButtons() {
    const codeBlocks = document.querySelectorAll('pre code');

    codeBlocks.forEach((codeBlock, index) => {
        const pre = codeBlock.parentElement;

        // Skip if already processed
        if (pre.classList.contains('has-copy-button')) {
            return;
        }

        // Create copy button
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
            <span class="copy-text">Copy</span>
        `;
        copyButton.setAttribute('aria-label', 'Copy code to clipboard');

        // Style the copy button
        copyButton.style.cssText = `
            position: absolute;
            top: 0.5rem;
            right: 0.5rem;
            background: var(--tertiary-color, #1e2749);
            border: 1px solid var(--border-color, #2a2f4a);
            border-radius: 4px;
            padding: 0.4rem 0.6rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.85rem;
            color: var(--text-color, #e4e4e7);
            transition: all 0.3s ease;
            opacity: 0;
            z-index: 10;
        `;

        // Make parent relative for positioning
        pre.style.position = 'relative';

        // Add hover effect
        pre.addEventListener('mouseenter', () => {
            copyButton.style.opacity = '1';
        });

        pre.addEventListener('mouseleave', () => {
            copyButton.style.opacity = '0';
        });

        // Add click handler
        copyButton.addEventListener('click', async () => {
            const code = codeBlock.textContent;
            const buttonText = copyButton.querySelector('.copy-text');

            try {
                await navigator.clipboard.writeText(code);

                // Visual feedback
                const originalText = buttonText.textContent;
                buttonText.textContent = 'Copied!';
                copyButton.style.background = 'var(--success-color, #00ff88)';
                copyButton.style.color = 'var(--primary-color, #0a0e27)';

                setTimeout(() => {
                    buttonText.textContent = originalText;
                    copyButton.style.background = 'var(--tertiary-color, #1e2749)';
                    copyButton.style.color = 'var(--text-color, #e4e4e7)';
                }, 2000);

            } catch (err) {
                console.error('Failed to copy:', err);
                buttonText.textContent = 'Failed!';
                copyButton.style.background = 'var(--danger-color, #ff4444)';

                setTimeout(() => {
                    buttonText.textContent = 'Copy';
                    copyButton.style.background = 'var(--tertiary-color, #1e2749)';
                    copyButton.style.color = 'var(--text-color, #e4e4e7)';
                }, 2000);
            }
        });

        // Append button to pre element
        pre.appendChild(copyButton);
        pre.classList.add('has-copy-button');
    });
}

/**
 * Add specific copy buttons to terminal blocks
 */
function addTerminalCopyButtons() {
    const terminalBlocks = document.querySelectorAll('.terminal');

    terminalBlocks.forEach(terminal => {
        if (terminal.classList.contains('has-copy-button')) {
            return;
        }

        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button terminal-copy';
        copyButton.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="16 18 22 12 16 6"></polyline>
                <polyline points="8 6 2 12 8 18"></polyline>
            </svg>
            <span>Copy Command</span>
        `;

        copyButton.style.cssText = `
            position: absolute;
            top: 0.5rem;
            right: 0.5rem;
            background: var(--tertiary-color, #1e2749);
            border: 1px solid var(--border-color, #2a2f4a);
            border-radius: 4px;
            padding: 0.4rem 0.6rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.85rem;
            color: var(--text-color, #e4e4e7);
            transition: all 0.3s ease;
            z-index: 10;
        `;

        terminal.style.position = 'relative';

        copyButton.addEventListener('click', async () => {
            const commands = terminal.textContent.split('\n').filter(line => line.trim());
            if (commands.length === 0) return;

            const firstCommand = commands[0].trim();
            try {
                await navigator.clipboard.writeText(firstCommand);
                copyButton.innerHTML = `<span>Copied!</span>`;
                setTimeout(() => {
                    copyButton.innerHTML = `
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="16 18 22 12 16 6"></polyline>
                            <polyline points="8 6 2 12 8 18"></polyline>
                        </svg>
                        <span>Copy Command</span>
                    `;
                }, 2000);
            } catch (err) {
                console.error('Failed to copy:', err);
            }
        });

        terminal.appendChild(copyButton);
        terminal.classList.add('has-copy-button');
    });
}

// Initialize terminal copy buttons
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(addTerminalCopyButtons, 500);
});
