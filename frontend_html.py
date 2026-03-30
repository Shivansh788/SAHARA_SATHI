import json

html_content = r"""<!DOCTYPE html>
<html class="light" lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Sahara Saathi | Empathetic Welfare Dashboard</title>
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/dompurify@3.1.6/dist/purify.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@200;300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet"/>
    <link href="https://fonts.googleapis.com/icon?family=Material+Symbols+Outlined" rel="stylesheet"/>
    <script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    colors: {
                        "primary": "#00003c",
                        "primary-container": "#000080",
                        "secondary": "#8f4e00",
                        "secondary-container": "#fe9832",
                        "secondary-fixed": "#ffdcc2",
                        "on-secondary-fixed": "#2e1500",
                        "on-surface": "#191c1e",
                        "on-surface-variant": "#464653",
                        "surface-container-lowest": "#ffffff",
                        "surface-container-low": "#f2f4f7",
                        "surface-container": "#eceef1",
                        "surface-container-high": "#e6e8eb",
                        "surface-container-highest": "#e0e3e6",
                        "outline": "#767684",
                        "outline-variant": "#c6c5d5",
                        "background": "#f7f9fc",
                        "primary-fixed": "#e0e0ff",
                        "on-primary-fixed": "#00006e"
                    },
                    fontFamily: {
                        "headline": ["Manrope"],
                        "body": ["Manrope"],
                        "label": ["Plus Jakarta Sans"]
                    }
                }
            }
        }
    </script>
    <style>
        .material-symbols-outlined {
            font-family: 'Material Symbols Outlined';
            font-weight: normal;
            font-style: normal;
            font-size: 24px;
            display: inline-block;
            line-height: 1;
            text-transform: none;
            letter-spacing: normal;
            word-wrap: normal;
            white-space: nowrap;
            direction: ltr;
            -webkit-font-smoothing: antialiased;
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
        }
        .premium-shadow {
            box-shadow: 0 32px 48px -12px rgba(25, 28, 30, 0.04);
        }
        body {
            font-family: 'Manrope', sans-serif;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        .animate-spin {
            animation: spin 1s linear infinite;
        }
        .hidden-view {
            display: none !important;
        }
        .chat-input-field:focus {
            outline: none;
        }
        /* ── Chat input bar polish ── */
        .chat-action-btn {
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            width: 48px;
            height: 48px;
            border-radius: 14px;
            border: 1.5px solid #e2e8f0;
            background: #ffffff;
            color: #64748b;
            cursor: pointer;
            transition: background 0.18s ease, color 0.18s ease, border-color 0.18s ease, transform 0.12s ease, box-shadow 0.18s ease;
        }
        .chat-action-btn:hover {
            background: #f0f4ff;
            color: #00003c;
            border-color: #c7d2fe;
            box-shadow: 0 2px 8px rgba(0,0,64,0.10);
        }
        .chat-action-btn:active {
            transform: scale(0.93);
            background: #e0e7ff;
        }
        .chat-send-btn {
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            width: 52px;
            height: 52px;
            border-radius: 16px;
            background: linear-gradient(135deg, #00003c 0%, #000080 100%);
            color: #ffffff;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 14px rgba(0,0,128,0.30);
            transition: background 0.18s ease, transform 0.12s ease, box-shadow 0.18s ease;
        }
        .chat-send-btn:hover {
            background: linear-gradient(135deg, #000080 0%, #0000b0 100%);
            box-shadow: 0 6px 20px rgba(0,0,128,0.40);
            transform: translateY(-1px);
        }
        .chat-send-btn:active {
            transform: scale(0.92) translateY(0);
            box-shadow: 0 2px 8px rgba(0,0,128,0.25);
        }
        .chat-mode-select {
            height: 52px;
            padding: 0 12px;
            border-radius: 14px;
            border: 1.5px solid #e2e8f0;
            background: #ffffff;
            font-size: 0.82rem;
            font-weight: 700;
            color: #374151;
            cursor: pointer;
            transition: border-color 0.18s ease, box-shadow 0.18s ease;
            appearance: none;
            -webkit-appearance: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%2364748b' stroke-width='1.5' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 10px center;
            padding-right: 28px;
        }
        .chat-mode-select:focus {
            outline: none;
            border-color: #000080;
            box-shadow: 0 0 0 3px rgba(0,0,128,0.10);
        }
        .chat-text-input {
            flex: 1;
            min-width: 0;
            height: 52px;
            padding: 0 20px;
            border-radius: 16px;
            border: 1.5px solid #e2e8f0;
            background: #ffffff;
            font-size: 0.97rem;
            color: #1e293b;
            box-shadow: 0 1px 4px rgba(0,0,0,0.05);
            transition: border-color 0.18s ease, box-shadow 0.18s ease;
        }
        .chat-text-input:focus {
            outline: none;
            border-color: #000080;
            box-shadow: 0 0 0 3px rgba(0,0,128,0.08), 0 1px 4px rgba(0,0,0,0.05);
        }
        .line-clamp-2 {
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        .line-clamp-3 {
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        #verified-badge { transition: opacity 0.3s; }
        #app-preloader {
            transition: opacity 0.45s ease, visibility 0.45s ease;
        }
        #app-preloader.preloader-hidden {
            opacity: 0;
            visibility: hidden;
            pointer-events: none;
        }
        #main-sidebar {
            transition: width 0.3s ease;
        }
        #main-content {
            transition: padding-left 0.3s ease;
        }
        #main-sidebar.sidebar-collapsed {
            width: 5rem;
        }
        @media (min-width: 768px) {
            #main-content.sidebar-collapsed {
                padding-left: 5rem;
            }
        }
        #main-sidebar.sidebar-collapsed .nav-label {
            width: 0;
            opacity: 0;
            overflow: hidden;
            pointer-events: none;
        }
        #main-sidebar.sidebar-collapsed .nav-link-side {
            justify-content: center;
            position: relative;
        }
        #main-sidebar.sidebar-collapsed .sidebar-hotline {
            display: none;
        }
        .sidebar-volunteer-btn {
            display: flex;
            align-items: center;
            gap: 10px;
            width: 88%;
            margin: 0 auto 12px auto;
            padding: 13px 18px;
            border-radius: 14px;
            background: #eef0ff;
            color: #00003c;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 0.82rem;
            font-weight: 800;
            letter-spacing: 0.01em;
            border: 1.5px solid #c7ccf5;
            cursor: pointer;
            transition: background 0.2s ease, box-shadow 0.2s ease, transform 0.15s ease;
            text-align: left;
            box-shadow: 0 2px 8px 0 rgba(0,0,60,0.06);
        }
        .sidebar-volunteer-btn:hover {
            background: #dde2ff;
            box-shadow: 0 4px 16px 0 rgba(0,0,60,0.12);
            transform: translateY(-1px);
        }
        .sidebar-volunteer-btn:active {
            transform: translateY(0);
            background: #c7ccf5;
        }
        #main-sidebar.sidebar-collapsed .sidebar-volunteer-btn {
            display: none;
        }
        #main-sidebar.sidebar-collapsed .nav-link-side::after {
            content: attr(data-tooltip);
            position: absolute;
            left: calc(100% + 10px);
            top: 50%;
            transform: translateY(-50%);
            background: #00003c;
            color: #ffffff;
            padding: 6px 10px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 700;
            white-space: nowrap;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.2s ease;
            z-index: 70;
        }
        #main-sidebar.sidebar-collapsed .nav-link-side:hover::after {
            opacity: 1;
        }
        .sidebar-hamburger-line {
            width: 18px;
            height: 2px;
            border-radius: 9999px;
            background: #00003c;
        }
        .ai-markdown {
            font-size: 1.15rem;
            line-height: 1.85;
            color: #1f2937;
        }
        .ai-markdown h1,
        .ai-markdown h2,
        .ai-markdown h3,
        .ai-markdown h4 {
            color: #00003c;
            font-family: 'Manrope', sans-serif;
            font-weight: 800;
            line-height: 1.4;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .ai-markdown h1 { font-size: 1.85rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; }
        .ai-markdown h2 { font-size: 1.6rem; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.4rem; }
        .ai-markdown h3 { font-size: 1.35rem; }
        .ai-markdown h4 { font-size: 1.15rem; }
        .ai-markdown p {
            margin: 0.75rem 0;
        }
        .ai-markdown ul,
        .ai-markdown ol {
            margin: 0.75rem 0 1rem 1.5rem;
        }
        .ai-markdown li {
            margin: 0.4rem 0;
        }
        .ai-markdown hr {
            margin: 1.5rem 0;
            border: 0;
            border-top: 2px dashed #e2e8f0;
        }
        .ai-markdown blockquote {
            margin: 1.25rem 0;
            padding: 1rem 1.25rem;
            border-left: 6px solid #fe9832;
            border-radius: 0.75rem;
            background: #fff7ed;
            color: #7c2d12;
            font-style: italic;
        }
        .ai-markdown a {
            color: #000080;
            font-weight: 800;
            text-decoration: underline;
            text-underline-offset: 3px;
        }
        .ai-markdown input[type="checkbox"] {
            width: 1.25rem;
            height: 1.25rem;
            accent-color: #fe9832;
            margin-right: 0.75rem;
        }
        .ai-markdown .amount-highlight {
            color: #c2410c;
            font-weight: 900;
            background: #ffedd5;
            border-radius: 0.5rem;
            padding: 0.1rem 0.5rem;
            border: 1px solid #fed7aa;
        }
        .card-container {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1.25rem;
            margin: 1.5rem 0;
        }
        .rich-card {
            background: white;
            border-radius: 1.5rem;
            padding: 1.5rem;
            border: 1px solid #e2e8f0;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }
        .rich-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
            border-color: #000080;
        }
        .rich-card-title {
            font-weight: 800;
            font-size: 1.25rem;
            color: #00003c;
            margin-bottom: 0.75rem;
        }
        .rich-card-detail {
            font-size: 0.95rem;
            color: #4b5563;
            margin-bottom: 0.5rem;
            display: flex;
            gap: 0.5rem;
        }
        .rich-card-detail b {
            color: #111827;
            min-width: 100px;
        }
        .rich-card-actions {
            margin-top: 1.25rem;
            display: flex;
            gap: 0.75rem;
        }
        .rich-card-btn {
            padding: 0.6rem 1.25rem;
            border-radius: 0.75rem;
            font-weight: 700;
            font-size: 0.85rem;
            transition: all 0.2s;
        }
        .btn-primary-card {
            background: #00003c;
            color: white;
        }
        .btn-primary-card:hover {
            background: #000080;
        }
        .btn-secondary-card {
            background: #f3f4f6;
            color: #374151;
            border: 1px solid #e5e7eb;
        }
        .btn-secondary-card:hover {
            background: #e5e7eb;
        }
        .rich-card-badge {
            display: inline-block;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.07em;
            text-transform: uppercase;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            background: #f0f4ff;
            color: #00003c;
            margin-bottom: 0.75rem;
        }
        .ngo-badge {
            background: #f0fdf4;
            color: #166534;
        }
        .ngo-title {
            color: #166534 !important;
        }
        .scheme-card {
            border-left: 5px solid #00003c;
        }
        .ngo-card {
            border-left: 5px solid #16a34a;
        }
        .detail-label {
            font-weight: 700;
            color: #374151;
            min-width: 130px;
            flex-shrink: 0;
        }
        .rich-card-detail {
            display: flex;
            gap: 0.5rem;
            align-items: flex-start;
            font-size: 0.97rem;
            color: #4b5563;
            margin-bottom: 0.6rem;
        }
        .deadline-row .deadline-badge {
            background: #fff0e6;
            color: #c2410c;
            font-weight: 800;
            border-radius: 0.5rem;
            padding: 0.1rem 0.6rem;
            border: 1px solid #fed7aa;
        }
    </style>
</head>
<body class="bg-background text-on-surface min-h-screen">

    <!-- ================= PRELOADER ================= -->
    <div id="app-preloader" class="fixed inset-0 z-[200] flex items-center justify-center bg-[#00003c] overflow-hidden">
        <video id="preloader-video" class="absolute inset-0 w-full h-full object-cover opacity-30" autoplay muted loop playsinline>
            <source src="/assets/preloader.mp4" type="video/mp4" />
            <source src="/assets/Prelaoder.mp4" type="video/mp4" />
        </video>
        <div class="absolute inset-0 bg-gradient-to-b from-[#00003c]/75 via-[#00003c]/80 to-[#00003c]/90"></div>
        <div class="relative z-10 flex flex-col items-center gap-4 px-6">
            <img src="/assets/sahara.svg" alt="Sahara logo" class="w-24 h-24 md:w-28 md:h-28 object-contain drop-shadow-[0_10px_30px_rgba(0,0,0,0.35)]" />
            <h1 class="text-white text-3xl md:text-4xl font-black tracking-tight">Sahara Saathi</h1>
            <p class="text-blue-100 text-sm md:text-base font-semibold text-center">Loading welfare intelligence for you...</p>
            <div class="w-44 h-1.5 rounded-full bg-white/20 overflow-hidden mt-1">
                <div class="h-full w-1/2 bg-orange-400 animate-pulse"></div>
            </div>
        </div>
    </div>

    <!-- ================= AUTH SCREEN ================= -->
    <div id="auth-screen" class="fixed inset-0 z-[100] bg-gradient-to-br from-[#00003c] via-[#000060] to-[#000080] flex items-center justify-center" style="display:none;">
        <div class="absolute inset-0 overflow-hidden pointer-events-none">
            <div class="absolute -top-40 -right-40 w-[500px] h-[500px] bg-orange-500/10 rounded-full blur-3xl"></div>
            <div class="absolute -bottom-40 -left-40 w-[600px] h-[600px] bg-blue-400/10 rounded-full blur-3xl"></div>
        </div>
        <div class="relative z-10 w-full max-w-md mx-4">
            <button onclick="hideAuthOverlay()" class="absolute -top-12 right-0 w-10 h-10 rounded-full bg-white/10 border border-white/20 text-white hover:bg-white/20 transition-colors flex items-center justify-center" aria-label="Close login overlay">
                <span class="material-symbols-outlined">close</span>
            </button>
            <!-- Logo -->
            <div class="text-center mb-10">
                <div class="w-16 h-16 bg-white/10 backdrop-blur-xl rounded-2xl flex items-center justify-center mx-auto mb-4 border border-white/20">
                    <span class="material-symbols-outlined text-white text-3xl" style="font-variation-settings: 'FILL' 1;">account_balance</span>
                </div>
                <h1 class="text-4xl font-black text-white tracking-tight font-['Manrope']">Sahara Saathi</h1>
                <p class="text-blue-200 text-sm mt-2 font-['Plus_Jakarta_Sans']">Empowering every citizen with accessible welfare solutions</p>
            </div>

            <!-- Login Form -->
            <div id="login-form" class="bg-white/10 backdrop-blur-2xl rounded-3xl p-8 border border-white/20 shadow-2xl">
                <h2 class="text-2xl font-bold text-white mb-6 font-['Manrope']">Welcome Back</h2>
                <div class="flex flex-col gap-5">
                    <div>
                        <label class="text-blue-200 text-xs font-bold uppercase tracking-widest mb-2 block font-['Plus_Jakarta_Sans']">Email Address</label>
                        <input id="login-id" type="email" placeholder="Enter your email" class="w-full h-14 px-5 bg-white/10 border border-white/20 rounded-xl text-white placeholder:text-blue-300/50 focus:outline-none focus:ring-2 focus:ring-orange-400/50 focus:border-orange-400/50 text-sm font-['Plus_Jakarta_Sans']"/>
                    </div>
                    <div>
                        <label class="text-blue-200 text-xs font-bold uppercase tracking-widest mb-2 block font-['Plus_Jakarta_Sans']">Password</label>
                        <input id="login-pass" type="password" placeholder="Enter your password" class="w-full h-14 px-5 bg-white/10 border border-white/20 rounded-xl text-white placeholder:text-blue-300/50 focus:outline-none focus:ring-2 focus:ring-orange-400/50 focus:border-orange-400/50 text-sm font-['Plus_Jakarta_Sans']"/>
                    </div>
                    <button onclick="handleLogin()" class="w-full h-14 bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-xl font-bold text-sm hover:from-orange-600 hover:to-orange-700 transition-all shadow-lg shadow-orange-500/30 flex items-center justify-center gap-2 font-['Plus_Jakarta_Sans']">
                        <span class="material-symbols-outlined text-lg">login</span>
                        Sign In
                    </button>
                    <button onclick="showOrgLogin()" class="w-full h-12 bg-white/10 text-white rounded-xl font-bold text-xs hover:bg-white/20 transition-all border border-white/20 flex items-center justify-center gap-2 font-['Plus_Jakarta_Sans']">
                        <span class="material-symbols-outlined text-base">admin_panel_settings</span>
                        Organization Admin Login
                    </button>
                </div>
                <div class="mt-6 text-center">
                    <p class="text-blue-200/70 text-sm font-['Plus_Jakarta_Sans']">Don't have an account? <a onclick="showSignup()" class="text-orange-400 font-bold cursor-pointer hover:underline">Create Account</a></p>
                </div>
            </div>

            <div id="org-login-form" class="bg-white/10 backdrop-blur-2xl rounded-3xl p-8 border border-white/20 shadow-2xl" style="display:none;">
                <h2 class="text-2xl font-bold text-white mb-6 font-['Manrope']">Organization Admin</h2>
                <div class="flex flex-col gap-4">
                    <div>
                        <label class="text-blue-200 text-xs font-bold uppercase tracking-widest mb-2 block font-['Plus_Jakarta_Sans']">Organization Email</label>
                        <input id="org-login-email" type="email" placeholder="Enter organization email" class="w-full h-14 px-5 bg-white/10 border border-white/20 rounded-xl text-white placeholder:text-blue-300/50 focus:outline-none focus:ring-2 focus:ring-orange-400/50 text-sm font-['Plus_Jakarta_Sans']"/>
                    </div>
                    <div>
                        <label class="text-blue-200 text-xs font-bold uppercase tracking-widest mb-2 block font-['Plus_Jakarta_Sans']">Password</label>
                        <input id="org-login-pass" type="password" placeholder="Enter organization password" class="w-full h-14 px-5 bg-white/10 border border-white/20 rounded-xl text-white placeholder:text-blue-300/50 focus:outline-none focus:ring-2 focus:ring-orange-400/50 text-sm font-['Plus_Jakarta_Sans']"/>
                    </div>
                    <button onclick="handleOrgLogin()" class="w-full h-14 bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-xl font-bold text-sm hover:from-orange-600 hover:to-orange-700 transition-all shadow-lg shadow-orange-500/30 flex items-center justify-center gap-2 font-['Plus_Jakarta_Sans']">
                        <span class="material-symbols-outlined text-lg">login</span>
                        Login as Admin
                    </button>
                </div>
                <div class="mt-6 text-center">
                    <p class="text-blue-200/70 text-sm font-['Plus_Jakarta_Sans']">Citizen account? <a onclick="showLogin()" class="text-orange-400 font-bold cursor-pointer hover:underline">Sign In</a></p>
                </div>
            </div>

            <!-- Signup Form -->
            <div id="signup-form" class="bg-white/10 backdrop-blur-2xl rounded-3xl p-8 border border-white/20 shadow-2xl" style="display:none;">
                <h2 class="text-2xl font-bold text-white mb-6 font-['Manrope']">Create Account</h2>
                <div class="flex flex-col gap-4">
                    <div>
                        <label class="text-blue-200 text-xs font-bold uppercase tracking-widest mb-2 block font-['Plus_Jakarta_Sans']">Full Name</label>
                        <input id="signup-name" type="text" placeholder="Enter your full name" class="w-full h-14 px-5 bg-white/10 border border-white/20 rounded-xl text-white placeholder:text-blue-300/50 focus:outline-none focus:ring-2 focus:ring-orange-400/50 text-sm font-['Plus_Jakarta_Sans']"/>
                    </div>
                    <div>
                        <label class="text-blue-200 text-xs font-bold uppercase tracking-widest mb-2 block font-['Plus_Jakarta_Sans']">Email Address</label>
                        <input id="signup-email" type="email" placeholder="Enter your email address" class="w-full h-14 px-5 bg-white/10 border border-white/20 rounded-xl text-white placeholder:text-blue-300/50 focus:outline-none focus:ring-2 focus:ring-orange-400/50 text-sm font-['Plus_Jakarta_Sans']"/>
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="text-blue-200 text-xs font-bold uppercase tracking-widest mb-2 block font-['Plus_Jakarta_Sans']">State</label>
                            <select id="signup-state" class="w-full h-14 px-5 bg-white/10 border border-white/20 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-orange-400/50 text-sm font-['Plus_Jakarta_Sans'] appearance-none">
                                <option value="" class="text-gray-900">Select</option>
                                <option value="Rajasthan" class="text-gray-900">Rajasthan</option>
                                <option value="Maharashtra" class="text-gray-900">Maharashtra</option>
                                <option value="UP" class="text-gray-900">Uttar Pradesh</option>
                                <option value="MP" class="text-gray-900">Madhya Pradesh</option>
                                <option value="Bihar" class="text-gray-900">Bihar</option>
                                <option value="WB" class="text-gray-900">West Bengal</option>
                                <option value="Karnataka" class="text-gray-900">Karnataka</option>
                                <option value="Tamil Nadu" class="text-gray-900">Tamil Nadu</option>
                                <option value="Gujarat" class="text-gray-900">Gujarat</option>
                                <option value="Odisha" class="text-gray-900">Odisha</option>
                            </select>
                        </div>
                        <div>
                            <label class="text-blue-200 text-xs font-bold uppercase tracking-widest mb-2 block font-['Plus_Jakarta_Sans']">Category</label>
                            <select id="signup-category" class="w-full h-14 px-5 bg-white/10 border border-white/20 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-orange-400/50 text-sm font-['Plus_Jakarta_Sans'] appearance-none">
                                <option value="" class="text-gray-900">Select</option>
                                <option value="General" class="text-gray-900">General</option>
                                <option value="OBC" class="text-gray-900">OBC</option>
                                <option value="SC" class="text-gray-900">SC</option>
                                <option value="ST" class="text-gray-900">ST</option>
                            </select>
                        </div>
                    </div>
                    <div>
                        <label class="text-blue-200 text-xs font-bold uppercase tracking-widest mb-2 block font-['Plus_Jakarta_Sans']">Password</label>
                        <input id="signup-pass" type="password" placeholder="Create a strong password" oninput="checkPasswordStrength(this.value)" class="w-full h-14 px-5 bg-white/10 border border-white/20 rounded-xl text-white placeholder:text-blue-300/50 focus:outline-none focus:ring-2 focus:ring-orange-400/50 text-sm font-['Plus_Jakarta_Sans']"/>
                        <!-- Password strength meter -->
                        <div class="mt-2">
                            <div class="flex gap-1 mb-1">
                                <div id="ps-bar-1" class="h-1 flex-1 rounded-full bg-white/20 transition-all duration-300"></div>
                                <div id="ps-bar-2" class="h-1 flex-1 rounded-full bg-white/20 transition-all duration-300"></div>
                                <div id="ps-bar-3" class="h-1 flex-1 rounded-full bg-white/20 transition-all duration-300"></div>
                                <div id="ps-bar-4" class="h-1 flex-1 rounded-full bg-white/20 transition-all duration-300"></div>
                            </div>
                            <p id="ps-hint" class="text-blue-300/70 text-xs font-['Plus_Jakarta_Sans']">Min 8 chars · uppercase · number · special char</p>
                        </div>
                    </div>
                    <button onclick="handleSignup()" class="w-full h-14 bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-xl font-bold text-sm hover:from-orange-600 hover:to-orange-700 transition-all shadow-lg shadow-orange-500/30 flex items-center justify-center gap-2 font-['Plus_Jakarta_Sans']">
                        <span class="material-symbols-outlined text-lg">person_add</span>
                        Create Account
                    </button>
                </div>
                <div class="mt-6 text-center">
                    <p class="text-blue-200/70 text-sm font-['Plus_Jakarta_Sans']">Already have an account? <a onclick="showLogin()" class="text-orange-400 font-bold cursor-pointer hover:underline">Sign In</a></p>
                </div>
            </div>
        </div>
    </div>

    <!-- Top Navigation Shell -->
    <header id="main-header" class="fixed top-0 w-full z-50 bg-white/70 backdrop-blur-xl shadow-sm shadow-blue-900/5 px-8 py-4 flex justify-between items-center">
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-white shadow-sm ring-1 ring-slate-200 flex items-center justify-center overflow-hidden">
                <img src="/assets/sahara.svg" alt="Sahara logo" class="w-8 h-8 object-contain" />
            </div>
            <span class="text-2xl font-black text-blue-900 font-['Manrope'] tracking-tight cursor-pointer" onclick="switchTab('home')">Sahara Saathi</span>
        </div>
        <div class="hidden md:flex items-center gap-3 text-slate-500 text-sm font-semibold">
            <span class="material-symbols-outlined text-base">menu_open</span>
            <span id="menu-guide-text">Use side menu to navigate</span>
        </div>
        <div class="flex items-center gap-4">
            <button id="lang-toggle" onclick="toggleLanguage()" class="px-3 py-1.5 bg-primary-fixed text-on-primary-fixed rounded-lg text-xs font-bold flex items-center gap-1.5 hover:bg-blue-100 transition-all font-['Plus_Jakarta_Sans'] hidden md:flex">
                <span class="material-symbols-outlined text-sm">translate</span>
                <span id="lang-label">English | हिंदी</span>
            </button>
            <button class="p-2 hover:bg-slate-100 rounded-full transition-colors hidden md:block" onclick="switchTab('schemes')">
                <span class="material-symbols-outlined text-on-surface-variant">search</span>
            </button>
            <button class="p-2 hover:bg-slate-100 rounded-full transition-colors relative" onclick="switchTab('applications')">
                <span class="material-symbols-outlined text-on-surface-variant">notifications</span>
                <span class="absolute top-2 right-2 w-2 h-2 bg-orange-500 rounded-full"></span>
            </button>
            <div id="guest-auth-actions" class="flex items-center gap-2">
                <button onclick="openAuth('login')" class="px-4 py-2 rounded-lg border border-slate-300 text-slate-700 text-xs font-bold hover:bg-white transition-all font-['Plus_Jakarta_Sans']">Login</button>
                <button onclick="openAuth('signup')" class="px-4 py-2 rounded-lg bg-primary text-white text-xs font-bold hover:bg-primary-container transition-all font-['Plus_Jakarta_Sans']">Sign Up</button>
            </div>
            <div id="user-profile-action" class="w-10 h-10 rounded-full overflow-hidden border-2 border-surface-container-highest cursor-pointer hidden-view" onclick="switchTab('profile')">
                <img alt="User Avatar" class="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDdyLbIIt_Y8J10gYHQ_tq_Upeo4xuAGg_roeL15PKrFg0s49sT2_ZlqEr1vciKI1JpK7ChTvKHgPxXOHObCqPkVTshvLrLJJzv1LiJpCVhJXTt13Z9uUjaQFj_UvwFikz7S0zQuRrKQ-iCbOBVITV8jURGxOF2oLMXO5Nf9Hi3wHDRwrPMO3Vb987JFGJR-d228y_97ptXdev6jashvk3rPhR1bGr6bSUnlJIlqGD3KuVWoR_l3tUywMb3GJnmErcaiTTGlMeilkfk"/>
            </div>
        </div>
    </header>

    <!-- Side Navigation (Mobile Hidden) -->
    <aside id="main-sidebar" class="h-screen w-72 fixed left-0 top-0 bg-slate-50 border-r border-outline-variant/10 pt-24 pb-8 flex flex-col z-40">
        <div class="px-4 md:px-6 flex flex-col gap-3 flex-1">
            <button id="sidebar-hamburger-btn" onclick="toggleSidebar(event)" class="w-10 h-10 rounded-lg bg-white border border-slate-200 text-primary hover:bg-slate-50 transition-all flex flex-col items-center justify-center gap-1 self-start" aria-label="Toggle sidebar">
                <span class="sidebar-hamburger-line"></span>
                <span class="sidebar-hamburger-line"></span>
                <span class="sidebar-hamburger-line"></span>
            </button>
            <div id="side-nav-items" class="flex flex-col gap-1">
                <a class="nav-link-side cursor-pointer flex items-center gap-4 px-4 py-3 rounded-xl text-blue-900 font-bold border-r-4 border-orange-500 bg-orange-50/50 transition-all duration-300" onclick="switchTab('home')" data-target="home" data-tooltip="Home">
                    <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">home</span>
                    <span class="nav-label font-['Plus_Jakarta_Sans'] text-sm">Home</span>
                </a>
                <a class="nav-link-side cursor-pointer flex items-center gap-4 px-4 py-3 rounded-xl text-slate-500 hover:text-blue-900 hover:bg-blue-50 transition-all duration-300" onclick="switchTab('schemes')" data-target="schemes" data-tooltip="Schemes">
                    <span class="material-symbols-outlined">account_balance</span>
                    <span class="nav-label font-['Plus_Jakarta_Sans'] text-sm">Schemes</span>
                </a>
                <a class="nav-link-side cursor-pointer flex items-center gap-4 px-4 py-3 rounded-xl text-slate-500 hover:text-blue-900 hover:bg-blue-50 transition-all duration-300" onclick="switchTab('applications')" data-target="applications" data-tooltip="Applications">
                    <span class="material-symbols-outlined">description</span>
                    <span class="nav-label font-['Plus_Jakarta_Sans'] text-sm">Applications</span>
                </a>
                <a class="nav-link-side cursor-pointer flex items-center gap-4 px-4 py-3 rounded-xl text-slate-500 hover:text-blue-900 hover:bg-blue-50 transition-all duration-300" onclick="switchTab('chat')" data-target="chat" data-tooltip="Chat Assistant">
                    <span class="material-symbols-outlined">forum</span>
                    <span class="nav-label font-['Plus_Jakarta_Sans'] text-sm">Chat Assistant</span>
                </a>
                <a class="nav-link-side cursor-pointer flex items-center gap-4 px-4 py-3 rounded-xl text-slate-500 hover:text-blue-900 hover:bg-blue-50 transition-all duration-300" onclick="switchTab('profile')" data-target="profile" data-tooltip="Profile">
                    <span class="material-symbols-outlined">person</span>
                    <span class="nav-label font-['Plus_Jakarta_Sans'] text-sm">Profile</span>
                </a>
                <a id="org-nav-item" class="nav-link-side cursor-pointer flex items-center gap-4 px-4 py-3 rounded-xl text-slate-500 hover:text-blue-900 hover:bg-orange-50 transition-all duration-300" onclick="switchTab('org-profile')" data-target="org-profile" data-tooltip="Org Dashboard" style="display:none;">
                    <span class="material-symbols-outlined text-orange-500" style="font-variation-settings: 'FILL' 1;">admin_panel_settings</span>
                    <span class="nav-label font-['Plus_Jakarta_Sans'] text-sm font-bold text-orange-600">Org Dashboard</span>
                </a>
            </div>
        </div>
        <div class="px-8 mt-auto sidebar-hotline">
            <button
                id="sidebar-volunteer-cta"
                class="sidebar-volunteer-btn"
                onclick="openAuth('login')"
                aria-label="Volunteer an Event"
            >
                <span class="material-symbols-outlined" style="font-size:18px; color:#00003c;">volunteer_activism</span>
                Volunteer an Event
            </button>
            <div class="p-4 bg-primary text-white rounded-2xl relative overflow-hidden group">
                <div class="relative z-10">
                    <p class="text-xs font-label opacity-70 mb-1">Assistance Hotlines</p>
                    <p class="font-bold text-sm">1800-SAHARA</p>
                </div>
                <div class="absolute -right-4 -bottom-4 opacity-10 group-hover:scale-110 transition-transform">
                    <span class="material-symbols-outlined text-6xl">support_agent</span>
                </div>
            </div>
        </div>
    </aside>

    <!-- Main Content Canvas -->
    <main id="main-content" class="md:pl-72 pt-24 min-h-screen">
        <div class="max-w-7xl mx-auto px-8 py-8 flex flex-col gap-12">

            <!-- ================= VIEW: HOME ================= -->
            <div id="view-home" class="view-section flex flex-col gap-12">
                <!-- Hero Search Section -->
                <section class="flex flex-col items-center text-center gap-8 py-12">
                    <div class="max-w-3xl flex flex-col gap-4">
                        <h1 class="text-5xl font-extrabold tracking-tighter text-primary font-headline">
                            Namaste, <span id="home-hero-name" class="text-secondary-container">Citizen</span>.
                        </h1>
                        <p class="text-on-surface-variant text-xl font-body leading-relaxed">
                            How can Sahara Saathi help you today? Explore benefits designed for your growth.
                        </p>
                    </div>
                    <div class="w-full max-w-4xl relative group">
                        <input id="mainSearchInput" class="w-full h-20 pl-8 pr-32 bg-surface-container-lowest rounded-full premium-shadow border-none focus:ring-4 focus:ring-primary/5 text-lg font-body placeholder:text-outline transition-all" placeholder="Search for schemes, services, or eligibility..." type="text" onkeypress="if(event.key === 'Enter') { switchTab('chat'); triggerRAGAPI(this.value); this.value=''; }"/>
                        <button onclick="switchTab('chat'); triggerRAGAPI(document.getElementById('mainSearchInput').value); document.getElementById('mainSearchInput').value='';" class="absolute right-3 top-3 bottom-3 px-8 bg-gradient-to-r from-primary to-primary-container text-white rounded-full font-bold flex items-center gap-2 hover:opacity-90 transition-all shadow-lg shadow-primary/20">
                            <span class="material-symbols-outlined">magnification_large</span>
                            Search
                        </button>
                    </div>
                    <div class="flex gap-3 overflow-x-auto pb-4 no-scrollbar">
                        <span class="cursor-pointer hover:bg-orange-200 px-4 py-2 bg-secondary-fixed text-on-secondary-fixed rounded-full text-xs font-bold whitespace-nowrap" onclick="switchTab('schemes')">Trending: PM-Kisan</span>
                        <span class="cursor-pointer hover:bg-slate-200 px-4 py-2 bg-surface-container-high text-on-surface-variant rounded-full text-xs font-medium whitespace-nowrap" onclick="switchTab('schemes')">Old Age Pension</span>
                        <span class="cursor-pointer hover:bg-slate-200 px-4 py-2 bg-surface-container-high text-on-surface-variant rounded-full text-xs font-medium whitespace-nowrap" onclick="switchTab('schemes')">Skill Development</span>
                    </div>
                </section>

                <!-- Dashboard Grid Area -->
                <div class="grid grid-cols-12 gap-8">
                    <!-- Left: Suggested Schemes & Stats -->
                    <div class="col-span-12 lg:col-span-8 flex flex-col gap-8">
                        <div class="flex justify-between items-end px-2">
                            <h2 class="text-2xl font-bold font-headline text-primary">Tailored for You</h2>
                            <button class="text-secondary font-bold text-sm hover:underline" onclick="switchTab('schemes')">View All Schemes</button>
                        </div>
                        <div class="grid md:grid-cols-2 gap-6" id="dashboard-scheme-cards">
                            <!-- Populated dynamically via cloning or static -->
                            <div class="scheme-card-template glass-card premium-shadow rounded-[2rem] p-8 border border-white/40 flex flex-col gap-6 relative overflow-hidden group h-full">
                                <div class="absolute top-0 right-0 w-32 h-32 bg-secondary-container/10 rounded-bl-full -mr-8 -mt-8"></div>
                                <div class="w-14 h-14 bg-secondary-fixed rounded-2xl flex items-center justify-center text-on-secondary-fixed">
                                    <span class="material-symbols-outlined text-3xl" style="font-variation-settings: 'FILL' 1;">agriculture</span>
                                </div>
                                <div class="flex-1">
                                    <h3 class="text-xl font-extrabold text-primary mb-2">PM-Kisan Samman Nidhi</h3>
                                    <p class="text-on-surface-variant text-sm leading-relaxed mb-6">Financial benefit of ₹6,000 per year in three equal installments to all landholding farmer families.</p>
                                    <div class="flex flex-wrap gap-2 mb-8">
                                        <span class="px-3 py-1 bg-green-100 text-green-700 rounded-lg text-[10px] font-bold uppercase tracking-wider">Eligible</span>
                                        <span class="px-3 py-1 bg-surface-container-high text-on-surface-variant rounded-lg text-[10px] font-bold uppercase tracking-wider">Direct Benefit Transfer</span>
                                    </div>
                                </div>
                                <button class="w-full py-4 bg-primary text-white rounded-xl font-bold text-sm hover:bg-primary-container transition-all" onclick="switchTab('chat'); triggerRAGAPI('How do I apply for PM-Kisan?');">Apply Now</button>
                            </div>
                            
                            <div class="scheme-card-template glass-card premium-shadow rounded-[2rem] p-8 border border-white/40 flex flex-col gap-6 relative overflow-hidden group h-full">
                                <div class="absolute top-0 right-0 w-32 h-32 bg-primary/5 rounded-bl-full -mr-8 -mt-8"></div>
                                <div class="w-14 h-14 bg-primary-fixed rounded-2xl flex items-center justify-center text-on-primary-fixed">
                                    <span class="material-symbols-outlined text-3xl" style="font-variation-settings: 'FILL' 1;">home_work</span>
                                </div>
                                <div class="flex-1">
                                    <h3 class="text-xl font-extrabold text-primary mb-2">PM Awas Yojana</h3>
                                    <p class="text-on-surface-variant text-sm leading-relaxed mb-6">Affordable housing for all by 2024. Providing central assistance for building homes with basic amenities.</p>
                                    <div class="flex flex-wrap gap-2 mb-8">
                                        <span class="px-3 py-1 bg-secondary-fixed text-on-secondary-fixed rounded-lg text-[10px] font-bold uppercase tracking-wider">High Priority</span>
                                        <span class="px-3 py-1 bg-surface-container-high text-on-surface-variant rounded-lg text-[10px] font-bold uppercase tracking-wider">Housing</span>
                                    </div>
                                </div>
                                <button class="w-full py-4 bg-surface-container-highest text-primary rounded-xl font-bold text-sm hover:bg-slate-200 transition-all" onclick="switchTab('chat'); triggerRAGAPI('What is the status of my PM Awas Yojana application?');">Check Status</button>
                            </div>
                        </div>

                        <!-- Lower Section -->
                        <div class="grid grid-cols-1 md:grid-cols-5 gap-6">
                            <div class="md:col-span-3 bg-surface-container-lowest rounded-[2rem] p-8 premium-shadow flex items-center gap-8 border border-outline-variant/5">
                                <div class="flex-1">
                                    <h4 class="text-lg font-bold text-primary mb-2">Benefit Tracker</h4>
                                    <p class="text-on-surface-variant text-sm mb-4">You have successfully received 4 of 5 benefits this cycle.</p>
                                    <div class="w-full h-2 bg-surface-container rounded-full overflow-hidden">
                                        <div class="w-[80%] h-full bg-secondary-container"></div>
                                    </div>
                                </div>
                                <div class="w-24 h-24 rounded-full border-8 border-orange-50/50 flex items-center justify-center">
                                    <span class="text-2xl font-black text-secondary">80%</span>
                                </div>
                            </div>
                            <div class="md:col-span-2 bg-gradient-to-br from-primary to-primary-container rounded-[2rem] p-8 premium-shadow text-white relative overflow-hidden">
                                <h4 class="text-lg font-bold mb-1 relative z-10">Application Success</h4>
                                <p class="text-xs opacity-70 mb-4 relative z-10">Real-time status</p>
                                <div class="text-4xl font-black mb-2 relative z-10">9.2k</div>
                                <p class="text-[10px] opacity-60 relative z-10">Schemes processed today in your district</p>
                                <span class="material-symbols-outlined absolute -right-4 -bottom-4 text-8xl opacity-10">verified</span>
                            </div>
                        </div>
                    </div>

                    <!-- Right: AI Assistant Snippet -->
                    <div class="col-span-12 lg:col-span-4 flex flex-col gap-6 cursor-pointer" onclick="switchTab('chat')">
                        <div class="bg-surface-container-lowest rounded-[2.5rem] premium-shadow border border-blue-100 flex flex-col h-[600px] overflow-hidden hover:shadow-2xl hover:shadow-blue-900/10 transition-shadow">
                            <div class="p-6 bg-slate-50 border-b border-outline-variant/10 flex items-center gap-4">
                                <div class="w-12 h-12 bg-secondary-container rounded-full flex items-center justify-center shadow-lg shadow-orange-500/20">
                                    <span class="material-symbols-outlined text-white" style="font-variation-settings: 'FILL' 1;">forum</span>
                                </div>
                                <div>
                                    <h3 class="font-bold text-primary">Sahara AI</h3>
                                    <div class="flex items-center gap-1.5">
                                        <span class="w-2 h-2 bg-green-500 rounded-full"></span>
                                        <span class="text-xs text-on-surface-variant font-label">Always here for you</span>
                                    </div>
                                </div>
                            </div>
                            <div class="flex-1 p-6 flex flex-col gap-6 overflow-y-auto bg-gradient-to-b from-white to-slate-50 pointer-events-none chat-message-box relative">
                                <!-- Chat preview -->
                                <div class="absolute inset-0 flex items-center justify-center bg-white/50 backdrop-blur-[1px] z-10 opacity-0 hover:opacity-100 transition-opacity">
                                    <span class="px-6 py-3 bg-primary text-white font-bold rounded-full shadow-lg">Open Chat Assistant</span>
                                </div>
                                <div class="flex flex-col gap-2 max-w-[90%]">
                                    <div id="mini-chat-greeting" class="bg-surface-container p-4 rounded-2xl rounded-tl-none text-sm text-on-surface leading-relaxed shadow-sm border border-slate-100">
                                        Hello! I see your profile is verified. Click anywhere here to enlarge our chat room and ask me any queries!
                                    </div>
                                </div>
                            </div>
                            <div class="p-6 bg-white border-t border-outline-variant/10 pointer-events-none">
                                <div class="relative">
                                    <input class="w-full h-12 pl-4 pr-12 bg-surface-container-low rounded-xl border-none text-sm font-label" placeholder="Chat with AI..." type="text" disabled/>
                                    <button class="absolute right-2 top-2 w-8 h-8 bg-primary rounded-lg text-white flex items-center justify-center">
                                        <span class="material-symbols-outlined text-sm">open_in_new</span>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                <!-- Nearby Help (NGO) Section -->
                <div class="col-span-12 mt-8">
                    <h4 class="text-lg font-bold text-primary mb-2" id="ngo-section-title">Nearby Help (NGOs)</h4>
                    <div id="dashboard-ngo-cards" class="grid grid-cols-1 md:grid-cols-3 gap-4"></div>
                </div>
                </div>
            </div>

            <!-- ================= VIEW: SCHEMES ================= -->
            <div id="view-schemes" class="view-section hidden-view flex flex-col gap-8">
                <div class="flex justify-between items-end">
                    <div>
                        <h2 class="text-4xl font-extrabold font-headline text-primary">All Schemes Explorer</h2>
                        <p class="text-on-surface-variant text-sm mt-2">Discover and apply for 100+ government welfare initiatives.</p>
                    </div>
                    <div class="flex gap-4 items-center">
                        <div class="flex bg-white rounded-xl p-1 shadow-sm border border-slate-100" id="pagination-controls">
                            <button onclick="fetchAndRenderSchemes(1)" id="btn-page-1" class="px-6 py-2 rounded-lg text-sm font-bold transition-all bg-primary text-white">Page 1</button>
                            <button onclick="fetchAndRenderSchemes(2)" id="btn-page-2" class="px-6 py-2 rounded-lg text-sm font-bold transition-all text-slate-500 hover:bg-slate-50">Page 2</button>
                        </div>
                    </div>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" id="schemes-grid-full">
                    <!-- Loaded dynamically via API -->
                </div>
                <!-- NGO Explorer Section -->
                <div class="mt-8">
                    <h3 class="text-2xl font-bold text-primary mb-4" id="ngo-explorer-title">Nearby Help (NGOs)</h3>
                    <div id="explore-ngo-cards" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"></div>
                </div>
                    <div class="col-span-full py-20 flex flex-col items-center justify-center text-slate-400 gap-4">
                        <span class="material-symbols-outlined animate-spin text-4xl">sync</span>
                        <p class="font-bold">Fetching latest schemes...</p>
                    </div>
                </div>
            </div>

            <!-- ================= VIEW: APPLICATIONS ================= -->
            <div id="view-applications" class="view-section hidden-view flex flex-col gap-8">
                <h2 class="text-4xl font-extrabold font-headline text-primary">Your Applications</h2>
                <div class="bg-white rounded-3xl premium-shadow p-8 border border-slate-100">
                    <h3 class="text-2xl font-bold mb-6 text-primary border-b pb-4">Status & Tracking</h3>
                    <div class="flex flex-col gap-6">
                        <div class="flex justify-between items-center p-6 bg-green-50 rounded-2xl border border-green-100">
                            <div>
                                <h4 class="font-bold text-green-900 text-lg">PM-Kisan Installment</h4>
                                <p class="text-sm text-green-700">Processed completely • Dec 12, 2025</p>
                            </div>
                            <span class="px-4 py-2 bg-green-200 text-green-800 rounded-full text-xs font-bold uppercase">Success</span>
                        </div>
                        <div class="flex justify-between items-center p-6 bg-orange-50 rounded-2xl border border-orange-100">
                            <div>
                                <h4 class="font-bold text-orange-900 text-lg">Solar Pump Subsidy</h4>
                                <p class="text-sm text-orange-700">Awaiting Sub-Divisional Approval • Since Mar 01, 2026</p>
                            </div>
                            <span class="px-4 py-2 bg-orange-200 text-orange-800 rounded-full text-xs font-bold uppercase animate-pulse">Pending</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ================= VIEW: NGO EVENTS ================= -->
            <div id="view-events" class="view-section hidden-view flex flex-col gap-8">
                <div class="flex flex-col md:flex-row md:items-end md:justify-between gap-4">
                    <div>
                        <h2 class="text-4xl font-extrabold font-headline text-primary">NGO Events Hub</h2>
                        <p class="text-on-surface-variant text-sm mt-2">Find verified community camps, legal aid drives, and support events near you.</p>
                    </div>
                    <button onclick="switchTab('profile')" class="px-5 py-3 rounded-xl bg-primary text-white font-bold text-sm hover:bg-primary-container transition-all">Create Event (Org Admin)</button>
                </div>

                <div class="bg-white rounded-3xl premium-shadow p-6 border border-slate-100">
                    <div class="grid md:grid-cols-4 gap-4">
                        <input id="events-category-filter" type="text" placeholder="Filter by category (e.g., Healthcare)" class="h-12 px-4 rounded-xl border border-slate-200"/>
                        <input id="events-location-filter" type="text" placeholder="Filter by location (e.g., Jaipur)" class="h-12 px-4 rounded-xl border border-slate-200"/>
                        <button onclick="applyEventsFilter()" class="h-12 px-5 rounded-xl bg-primary text-white font-bold text-sm hover:bg-primary-container transition-all">Apply Filters</button>
                        <button onclick="clearEventsFilter()" class="h-12 px-5 rounded-xl border border-slate-300 text-slate-700 font-bold text-sm hover:bg-slate-50 transition-all">Clear</button>
                    </div>
                </div>

                <div id="events-grid-full" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"></div>
            </div>

            <!-- ================= VIEW: CHAT ASSISTANT ================= -->
            <div id="view-chat" class="view-section hidden-view flex flex-col h-[calc(100vh-140px)] px-1 sm:px-2 md:px-3 lg:px-4">
                <div class="flex-1 bg-surface-container-lowest rounded-[2.5rem] premium-shadow border border-slate-100 flex flex-col overflow-hidden max-w-6xl w-full mx-auto">
                    <div class="p-6 bg-primary border-b border-primary-container flex items-center justify-between">
                        <div class="flex items-center gap-4">
                            <div class="w-12 h-12 bg-white rounded-full flex items-center justify-center shadow-lg">
                                <span class="material-symbols-outlined text-primary" style="font-variation-settings: 'FILL' 1;">forum</span>
                            </div>
                            <div>
                                <h3 class="font-bold text-white text-xl">Sahara AI</h3>
                                <div class="flex items-center gap-1.5">
                                    <span class="w-2 h-2 bg-green-400 rounded-full"></span>
                                    <span class="text-sm text-blue-100 font-label">Ready to help across 100+ state schemas</span>
                                </div>
                            </div>
                        </div>
                        <div class="text-white bg-white/10 px-4 py-2 rounded-lg text-sm flex items-center gap-2 cursor-pointer hover:bg-white/20" onclick="window.chatSessionId = undefined; document.querySelectorAll('.chat-message-box').forEach(el=>el.innerHTML=''); appendBotMessage('Session cleared. How can I help you today?');">
                            <span class="material-symbols-outlined text-sm">refresh</span> New Session
                        </div>
                    </div>
                    
                    <!-- Chat Box -->
                    <div id="mainChatBox" class="chat-message-box flex-1 p-8 flex flex-col gap-6 overflow-y-auto bg-slate-50">
                        <!-- Standard welcome initialized via JS -->
                    </div>

                    <!-- Chat Input -->
                    <div class="px-5 py-4 bg-white border-t border-slate-100 shadow-[0_-10px_40px_rgba(0,0,0,0.03)] focus-within:bg-blue-50/20 transition-colors">
                        <div class="flex items-center gap-3">
                            <!-- Voice input -->
                            <button id="voice-input-btn" onclick="startVoiceInput()" class="chat-action-btn" title="बोलें" aria-label="Voice input">
                                <span class="material-symbols-outlined" style="font-size:22px;">mic</span>
                            </button>
                            <!-- Speak last answer -->
                            <button id="speak-last-btn" onclick="speakLastAnswer()" class="chat-action-btn" title="Listen to last answer" aria-label="Speak answer">
                                <span class="material-symbols-outlined" style="font-size:22px;">volume_up</span>
                            </button>
                            <!-- Main text input -->
                            <input id="actualChatInput" class="chat-text-input chat-input-field font-label" placeholder="यहाँ अपना सवाल लिखें..." type="text" onkeypress="if(event.key==='Enter'){triggerRAGAPI(this.value);this.value='';}" aria-label="Chat input"/>
                            <!-- Mode selector -->
                            <select id="chat-mode-select" class="chat-mode-select" onchange="window.currentMode=this.value" aria-label="Chat mode">
                                <option value="citizen">Citizen</option>
                                <option value="worker">Worker</option>
                                <option value="explorer">Explorer</option>
                            </select>
                            <!-- Send button — no longer absolute, sits inline -->
                            <button id="chat-send-btn" onclick="triggerRAGAPI(document.getElementById('actualChatInput').value); document.getElementById('actualChatInput').value='';" class="chat-send-btn" aria-label="Send message" title="Send">
                                <span class="material-symbols-outlined" style="font-size:22px;">send</span>
                            </button>
                        </div>
                        <div class="flex justify-center mt-3 text-xs text-slate-400 gap-6">
                            <span class="flex items-center gap-1.5"><span class="material-symbols-outlined" style="font-size:13px;">lock</span> Encrypted specific to your profile</span>
                            <span class="flex items-center gap-1.5 cursor-pointer hover:text-primary transition-colors"><span class="material-symbols-outlined" style="font-size:13px;">mic</span> English / हिंदी Voice input</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ================= VIEW: PROFILE ================= -->
            <div id="view-profile" class="view-section hidden-view flex flex-col gap-8">
                <h2 class="text-4xl font-extrabold font-headline text-primary flex items-center gap-4">
                    Citizen Profile
                    <button class="ml-2 px-3 py-1.5 bg-primary text-white rounded-lg text-xs font-bold flex items-center gap-1.5 hover:bg-blue-900 transition-all font-['Plus_Jakarta_Sans']">
                        <span class="material-symbols-outlined text-sm">edit</span>
                        Edit
                    </button>
                </h2>
                <div class="grid md:grid-cols-3 gap-8">
                    <!-- Profile Card -->
                    <div class="col-span-1 bg-white p-8 rounded-[2rem] premium-shadow border border-slate-100 flex flex-col items-center text-center gap-4">
                        <div class="w-32 h-32 rounded-full overflow-hidden border-4 border-primary">
                            <img alt="User Avatar" class="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDdyLbIIt_Y8J10gYHQ_tq_Upeo4xuAGg_roeL15PKrFg0s49sT2_ZlqEr1vciKI1JpK7ChTvKHgPxXOHObCqPkVTshvLrLJJzv1LiJpCVhJXTt13Z9uUjaQFj_UvwFikz7S0zQuRrKQ-iCbOBVITV8jURGxOF2oLMXO5Nf9Hi3wHDRwrPMO3Vb987JFGJR-d228y_97ptXdev6jashvk3rPhR1bGr6bSUnlJIlqGD3KuVWoR_l3tUywMb3GJnmErcaiTTGlMeilkfk"/>
                        </div>
                        <div>
                            <h3 id="profile-name-card" class="font-black text-2xl text-primary mt-2">Citizen</h3>
                            <p id="profile-id-card" class="text-on-surface-variant">ID: N/A</p>
                        </div>
                        <div class="flex items-center gap-2 bg-green-100 text-green-700 px-4 py-2 rounded-full text-sm font-bold mt-2">
                            <span class="material-symbols-outlined text-base" style="font-variation-settings: 'FILL' 1;">verified</span> Verified Citizen
                        </div>
                        <div class="flex gap-3 mt-4">
                            <button id="profile-speak-btn" onclick="speakProfileInfo()" class="w-12 h-12 rounded-full border border-slate-200 text-slate-400 hover:text-primary hover:bg-slate-50 flex items-center justify-center transition-all" title="Speak profile info">
                                <span class="material-symbols-outlined">volume_up</span>
                            </button>
                        </div>
                    </div>
                    <!-- Info Card -->
                    <div class="col-span-2 bg-white p-8 rounded-[2rem] premium-shadow border border-slate-100">
                        <h4 class="text-xl font-bold border-b pb-4 mb-6">Personal Details</h4>
                        <div class="grid grid-cols-2 gap-y-6 gap-x-12">
                            <div>
                                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Full Name</p>
                                <p id="profile-name-detail" class="font-bold text-primary">Citizen</p>
                            </div>
                            <div>
                                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Gender</p>
                                <p class="font-bold text-primary">Male</p>
                            </div>
                            <div>
                                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Date of Birth</p>
                                <p class="font-bold text-primary">12/03/1985</p>
                            </div>
                            <div>
                                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Email</p>
                                <p class="font-bold text-primary">Not provided</p>
                            </div>
                            <div>
                                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Phone Number</p>
                                <p class="font-bold text-primary">+91 98xxx xxxx2</p>
                            </div>
                            <div>
                                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">State</p>
                                <p id="profile-state-detail" class="font-bold text-primary">Rajasthan</p>
                            </div>
                            <div>
                                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">District</p>
                                <p class="font-bold text-primary">Jaipur</p>
                            </div>
                            <div>
                                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Category</p>
                                <p id="profile-category-detail" class="font-bold text-primary">OBC</p>
                            </div>
                            <div class="col-span-2">
                                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Address</p>
                                <p class="font-bold text-primary">123, Shastri Nagar, Jaipur, Rajasthan, 302016</p>
                            </div>
                            <div class="col-span-2">
                                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Occupation</p>
                                <p class="font-bold text-primary">Agriculture</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="bg-white p-8 rounded-[2rem] premium-shadow border border-slate-100">
                    <h4 class="text-xl font-bold border-b pb-4 mb-6">Saved Schemes</h4>
                    <div id="profile-bookmarks" class="flex flex-col gap-3 text-sm text-slate-600">
                        <span>No saved schemes yet.</span>
                    </div>
                </div>

                <!-- Create Event CTA -->
                <div class="bg-gradient-to-r from-[#00003c] to-[#000080] p-8 rounded-[2rem] premium-shadow border border-blue-900/20 flex flex-col md:flex-row items-center justify-between gap-6">
                    <div class="flex items-center gap-5">
                        <div class="w-14 h-14 bg-white/10 rounded-2xl flex items-center justify-center flex-shrink-0">
                            <span class="material-symbols-outlined text-white text-3xl" style="font-variation-settings: 'FILL' 1;">volunteer_activism</span>
                        </div>
                        <div>
                            <h4 class="text-xl font-bold text-white">Want to Create a Community Event?</h4>
                            <p class="text-blue-200 text-sm mt-1">Register your NGO or organization to host and manage events for citizens.</p>
                        </div>
                    </div>
                    <button
                        id="profile-create-event-btn"
                        onclick="switchTab('events')"
                        class="flex-shrink-0 flex items-center gap-2 px-8 py-4 bg-orange-500 hover:bg-orange-600 text-white font-bold rounded-2xl transition-all shadow-lg shadow-orange-500/30 hover:shadow-orange-500/50 hover:-translate-y-0.5 transform text-sm font-['Plus_Jakarta_Sans']"
                    >
                        <span class="material-symbols-outlined text-lg">add_circle</span>
                        Create Event
                    </button>
                </div>

                <div id="org-admin-panel" class="bg-white p-8 rounded-[2rem] premium-shadow border border-slate-100 hidden-view">
                    <div class="flex items-center justify-between gap-4 border-b pb-4 mb-6">
                        <div>
                            <h4 class="text-xl font-bold text-primary">Organization Event Admin</h4>
                            <p id="org-admin-subtitle" class="text-sm text-slate-500 mt-1">Login as organization admin to create events.</p>
                        </div>
                    </div>
                    <div class="grid md:grid-cols-2 gap-4">
                        <input id="event-title" type="text" placeholder="Event title (e.g., Healthcare Camp)" class="h-12 px-4 rounded-xl border border-slate-200"/>
                        <input id="event-category" type="text" placeholder="Category (e.g., Healthcare)" class="h-12 px-4 rounded-xl border border-slate-200"/>
                        <input id="event-location" type="text" placeholder="Location (e.g., Dehradun)" class="h-12 px-4 rounded-xl border border-slate-200"/>
                        <input id="event-start" type="date" class="h-12 px-4 rounded-xl border border-slate-200"/>
                        <input id="event-end" type="date" class="h-12 px-4 rounded-xl border border-slate-200"/>
                        <div></div>
                        <textarea id="event-description" placeholder="Event details" class="md:col-span-2 min-h-28 px-4 py-3 rounded-xl border border-slate-200"></textarea>
                    </div>
                    <div class="flex gap-3 mt-5">
                        <button onclick="createOrgEvent()" class="px-6 py-3 rounded-xl bg-primary text-white font-bold text-sm hover:bg-primary-container">Create Event</button>
                        <button onclick="openAuth('org-login')" class="px-6 py-3 rounded-xl border border-slate-300 text-slate-700 font-bold text-sm hover:bg-slate-50">Admin Login</button>
                    </div>
                </div>
            </div>

            <!-- ================= VIEW: ORG PROFILE ================= -->
            <div id="view-org-profile" class="view-section hidden-view flex flex-col gap-8">
                <div class="flex items-center justify-between flex-wrap gap-4">
                    <h2 class="text-4xl font-extrabold font-headline text-primary flex items-center gap-3">
                        <span class="material-symbols-outlined text-4xl" style="font-variation-settings: 'FILL' 1;">admin_panel_settings</span>
                        Organization Dashboard
                    </h2>
                    <button onclick="openCreateEventModal()" class="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-orange-500 to-orange-600 text-white font-bold rounded-2xl text-sm hover:from-orange-600 hover:to-orange-700 transition-all shadow-lg shadow-orange-500/30 hover:-translate-y-0.5 transform font-['Plus_Jakarta_Sans']">
                        <span class="material-symbols-outlined text-lg">add_circle</span>
                        Create Event
                    </button>
                </div>
                <div class="grid md:grid-cols-3 gap-8">
                    <div class="col-span-1 bg-white p-8 rounded-[2rem] premium-shadow border border-slate-100 flex flex-col items-center text-center gap-4">
                        <div class="w-24 h-24 rounded-2xl bg-gradient-to-br from-primary to-primary-container flex items-center justify-center">
                            <span class="material-symbols-outlined text-white text-5xl" style="font-variation-settings: 'FILL' 1;">corporate_fare</span>
                        </div>
                        <div>
                            <h3 id="org-profile-name" class="font-black text-2xl text-primary mt-2">Organization</h3>
                            <p id="org-profile-email" class="text-on-surface-variant text-sm mt-1">—</p>
                        </div>
                        <div class="flex items-center gap-2 bg-green-100 text-green-700 px-4 py-2 rounded-full text-sm font-bold">
                            <span class="material-symbols-outlined text-base" style="font-variation-settings: 'FILL' 1;">verified</span>
                            Verified Organization
                        </div>
                    </div>
                    <div class="col-span-2 bg-white p-8 rounded-[2rem] premium-shadow border border-slate-100">
                        <h4 class="text-xl font-bold border-b pb-4 mb-6">Organization Details</h4>
                        <div class="grid grid-cols-2 gap-y-6 gap-x-12">
                            <div>
                                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Organization Name</p>
                                <p id="org-detail-name" class="font-bold text-primary">—</p>
                            </div>
                            <div>
                                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Category</p>
                                <p id="org-detail-category" class="font-bold text-primary">—</p>
                            </div>
                            <div>
                                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Location</p>
                                <p id="org-detail-location" class="font-bold text-primary">—</p>
                            </div>
                            <div>
                                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Email</p>
                                <p id="org-detail-email" class="font-bold text-primary">—</p>
                            </div>
                            <div>
                                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Status</p>
                                <span class="inline-flex items-center gap-1.5 px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-bold">
                                    <span class="material-symbols-outlined text-sm" style="font-variation-settings:'FILL' 1;">check_circle</span>Verified
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="bg-white p-8 rounded-[2rem] premium-shadow border border-slate-100">
                    <div class="flex items-center justify-between mb-6 border-b pb-4">
                        <h4 class="text-xl font-bold">My Events</h4>
                        <button onclick="loadOrgEvents()" class="text-sm text-primary font-bold hover:underline flex items-center gap-1">
                            <span class="material-symbols-outlined text-base">refresh</span>Refresh
                        </button>
                    </div>
                    <div id="org-events-list" class="flex flex-col gap-4">
                        <p class="text-slate-400 text-sm">No events yet. Click "Create Event" to add one!</p>
                    </div>
                </div>
                <div class="flex justify-end">
                    <button onclick="orgLogout()" class="flex items-center gap-2 px-5 py-2.5 border border-red-200 text-red-600 rounded-xl font-bold text-sm hover:bg-red-50 transition-all">
                        <span class="material-symbols-outlined text-base">logout</span>
                        Logout Organization
                    </button>
                </div>
            </div>

            <!-- ================= CREATE EVENT MODAL ================= -->
            <div id="create-event-modal" class="fixed inset-0 z-[150] items-center justify-center" style="display:none;">
                <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" onclick="closeCreateEventModal()"></div>
                <div class="relative z-10 w-full max-w-lg mx-auto mt-20 bg-white rounded-3xl shadow-2xl p-8 flex flex-col gap-6">
                    <div class="flex items-center justify-between">
                        <h3 class="text-2xl font-black text-primary">Create New Event</h3>
                        <button onclick="closeCreateEventModal()" class="w-9 h-9 rounded-full bg-slate-100 hover:bg-slate-200 flex items-center justify-center transition-all">
                            <span class="material-symbols-outlined text-slate-600">close</span>
                        </button>
                    </div>
                    <div class="flex flex-col gap-4">
                        <div>
                            <label class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1 block">Event Name *</label>
                            <input id="modal-event-title" type="text" placeholder="e.g., Free Healthcare Camp" class="w-full h-12 px-4 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-200 text-sm font-['Plus_Jakarta_Sans']"/>
                        </div>
                        <div>
                            <label class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1 block">Description *</label>
                            <textarea id="modal-event-description" placeholder="Describe what the event is about..." class="w-full min-h-24 px-4 py-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-200 text-sm font-['Plus_Jakarta_Sans'] resize-none"></textarea>
                        </div>
                        <div>
                            <label class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1 block">Location *</label>
                            <input id="modal-event-location" type="text" placeholder="City / Area" class="w-full h-12 px-4 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-200 text-sm font-['Plus_Jakarta_Sans']"/>
                        </div>
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1 block">Start Date</label>
                                <input id="modal-event-start" type="date" class="w-full h-12 px-4 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-200 text-sm font-['Plus_Jakarta_Sans']"/>
                            </div>
                            <div>
                                <label class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1 block">End Date</label>
                                <input id="modal-event-end" type="date" class="w-full h-12 px-4 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-200 text-sm font-['Plus_Jakarta_Sans']"/>
                            </div>
                        </div>
                    </div>
                    <div class="flex gap-3 pt-2">
                        <button onclick="submitCreateEvent()" id="modal-submit-btn" class="flex-1 h-12 bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-xl font-bold text-sm hover:from-orange-600 hover:to-orange-700 transition-all shadow-lg shadow-orange-500/30 flex items-center justify-center gap-2 font-['Plus_Jakarta_Sans']">
                            <span class="material-symbols-outlined text-lg">add_circle</span>
                            Create Event
                        </button>
                        <button onclick="closeCreateEventModal()" class="px-6 h-12 border border-slate-200 text-slate-700 rounded-xl font-bold text-sm hover:bg-slate-50 transition-all font-['Plus_Jakarta_Sans']">
                            Cancel
                        </button>
                    </div>
                </div>
            </div>

            <!-- Footer Section (Only shows on Home/Schemes) -->
            <footer id="main-footer" class="mt-8 py-12 border-t border-outline-variant/10 grid grid-cols-1 md:grid-cols-4 gap-8">
                <div class="col-span-1 flex flex-col gap-4">
                    <span class="text-xl font-black text-primary">Sahara Saathi</span>
                    <p class="text-sm text-on-surface-variant leading-relaxed">Empowering every citizen with transparent, accessible, and empathetic government welfare solutions.</p>
                </div>
                <div class="flex flex-col gap-4">
                    <h5 class="font-bold text-primary text-sm">Resources</h5>
                    <a class="text-sm text-on-surface-variant hover:text-secondary" href="#">Tutorials</a>
                    <a class="text-sm text-on-surface-variant hover:text-secondary" href="#">FAQs</a>
                </div>
                <div class="flex flex-col gap-4">
                <h5 class="font-bold text-primary text-sm">Legal</h5>
                    <a class="text-sm text-on-surface-variant hover:text-secondary" href="#">Privacy Policy</a>
                    <a class="text-sm text-on-surface-variant hover:text-secondary" href="#">Terms of Service</a>
                </div>
            </footer>
        </div>
    </main>

    <!-- Success Badge Fixed -->
    <div id="verified-badge" class="fixed bottom-8 left-1/2 -translate-x-1/2 md:translate-x-0 md:left-auto md:right-8 z-50 pointer-events-none" style="display:none;">
        <div class="bg-secondary-fixed text-on-secondary-fixed px-6 py-3 rounded-full premium-shadow flex items-center gap-3 border border-secondary-container/20">
            <span class="material-symbols-outlined text-xl" style="font-variation-settings: 'FILL' 1;">verified_user</span>
            <span class="text-sm font-bold font-label">Your profile is 100% verified</span>
        </div>
    </div>

    <div id="toast-container" class="fixed top-6 right-6 z-[120] flex flex-col gap-3"></div>

    <!-- JAVASCRIPT LOGIC -->
    <script>
                        function showToast(message, type = 'info') {
                            const container = document.getElementById('toast-container');
                            if (!container) return;
                            const color = type === 'error'
                                ? 'bg-red-50 border-red-200 text-red-700'
                                : type === 'success'
                                    ? 'bg-green-50 border-green-200 text-green-700'
                                    : 'bg-blue-50 border-blue-200 text-blue-700';
                            const item = document.createElement('div');
                            item.className = `px-4 py-3 rounded-xl border shadow-md text-sm font-semibold ${color}`;
                            item.textContent = message;
                            container.appendChild(item);
                            setTimeout(() => {
                                item.style.opacity = '0';
                                item.style.transform = 'translateY(-6px)';
                                item.style.transition = 'all 0.3s ease';
                            }, 2200);
                            setTimeout(() => item.remove(), 2600);
                        }

                        // Profile speak logic
                        async function speakProfileInfo(buttonEl) {
                            // Gather profile info as a string
                            const p = window.currentUser || {};
                            const info = [
                                `Full Name: ${p.full_name || 'Citizen'}`,
                                'Gender: Male',
                                'Date of Birth: 12/03/1985',
                                `Email: ${p.identifier || 'Not provided'}`,
                                'Phone Number: +91 98xxx xxxx2',
                                `State: ${p.state || 'Rajasthan'}`,
                                'District: Jaipur',
                                `Category: ${p.category || 'OBC'}`,
                                'Address: 123, Shastri Nagar, Jaipur, Rajasthan, 302016',
                                'Occupation: Agriculture'
                            ].join('. ');
                            await playTTS(info, buttonEl || document.getElementById('profile-speak-btn'));
                        }

                        async function playTTS(text, buttonEl) {
                            if (!text || !text.trim()) return;
                            if (window.isSpeaking) return;

                            window.isSpeaking = true;
                            if (buttonEl) {
                                buttonEl.disabled = true;
                                buttonEl.classList.add('opacity-60', 'cursor-not-allowed');
                            }

                            try {
                                const response = await fetch('/api/tts', {
                                    method: 'POST',
                                    headers: { 'Content-Type': 'application/json' },
                                    body: JSON.stringify({
                                        text: text.replace(/<[^>]*>/g, ''),
                                        language: window.currentLanguage
                                    })
                                });

                                const data = await response.json();
                                if (!data.audio_base64) {
                                    appendBotMessage(t('askError'));
                                    return;
                                }

                                const mime = data.audio_mime || 'audio/mpeg';
                                const audio = new Audio(`data:${mime};base64,${data.audio_base64}`);
                                window.currentAudio = audio;

                                const resetSpeaking = () => {
                                    window.isSpeaking = false;
                                    if (buttonEl) {
                                        buttonEl.disabled = false;
                                        buttonEl.classList.remove('opacity-60', 'cursor-not-allowed');
                                    }
                                };

                                audio.addEventListener('ended', resetSpeaking, { once: true });
                                audio.addEventListener('error', resetSpeaking, { once: true });

                                await audio.play();
                            } catch (error) {
                                console.error(error);
                                window.isSpeaking = false;
                                if (buttonEl) {
                                    buttonEl.disabled = false;
                                    buttonEl.classList.remove('opacity-60', 'cursor-not-allowed');
                                }
                                showToast(t('connectionError'), 'error');
                            }
                        }

                        function speakMessageFromEncoded(encodedText, buttonEl) {
                            const text = decodeURIComponent(encodedText || '');
                            playTTS(text, buttonEl);
                        }

                        function speakMessageById(messageId, buttonEl) {
                            const text = (window.botMessageStore && window.botMessageStore[messageId]) || '';
                            if (!text) {
                                showToast('Could not find message text to speak.', 'error');
                                return;
                            }
                            playTTS(text, buttonEl);
                        }
                // Fetch and render NGOs for Home and Schemes
                async function fetchAndRenderNGOs(targetId, limit = 10) {
                    const container = document.getElementById(targetId);
                    if (!container) return;
                    container.innerHTML = `<span class='text-slate-400'>${window.currentLanguage === 'hindi' ? 'एनजीओ लोड हो रहे हैं...' : window.currentLanguage === 'hinglish' ? 'NGO load ho rahe hain...' : 'Loading NGOs...'}</span>`;

                    // Pass the user's state/location to filter NGOs near them
                    const u = window.currentUser || {};
                    const location = encodeURIComponent(u.state || u.location || 'Rajasthan');
                    const category = encodeURIComponent(u.category || '');

                    try {
                        const response = await fetch(`/api/ngos?location=${location}&category=${category}&limit=${limit}`);
                        const data = await response.json();
                        let ngos = data.ngos || [];
                        if (ngos.length === 0) {
                            container.innerHTML = `<span class='text-slate-400'>${window.currentLanguage === 'hindi' ? 'कोई एनजीओ नहीं मिला।' : window.currentLanguage === 'hinglish' ? 'Koi NGO nahi mila.' : 'No NGOs found.'}</span>`;
                            return;
                        }
                        container.innerHTML = '';
                        ngos.forEach(ngo => {
                            container.innerHTML += createNGOCard(ngo);
                        });
                    } catch (err) {
                        container.innerHTML = `<span class='text-red-400 font-bold'>${window.currentLanguage === 'hindi' ? 'एनजीओ लोड करने में त्रुटि।' : window.currentLanguage === 'hinglish' ? 'NGO load karne mein error.' : 'Error loading NGOs.'}</span>`;
                    }
                }

                function createNGOCard(ngo) {
                    // Translate fields if needed
                    const name = translateValue(ngo.name, window.currentLanguage);
                    const category = translateValue(ngo.category, window.currentLanguage);
                    const desc = translateValue(ngo.description, window.currentLanguage);
                    const location = translateValue(ngo.location, window.currentLanguage);
                    const eligibility = translateValue(ngo.eligibility, window.currentLanguage);
                    return `
                        <div class="glass-card premium-shadow rounded-2xl p-6 border border-white/40 flex flex-col gap-3 h-full">
                            <div class="flex items-center gap-3 mb-2">
                                <span class="material-symbols-outlined text-2xl text-secondary">volunteer_activism</span>
                                <span class="font-bold text-primary text-lg">${name}</span>
                            </div>
                            <div class="text-xs text-on-surface-variant mb-1"><b>${t('Category') || 'Category'}:</b> ${category}</div>
                            <div class="text-xs text-on-surface-variant mb-1"><b>${t('Location') || 'Location'}:</b> ${location}</div>
                            <div class="text-xs text-on-surface-variant mb-1"><b>${t('Eligibility') || 'Eligibility'}:</b> ${eligibility}</div>
                            <div class="text-sm text-on-surface-variant mb-2">${desc}</div>
                        </div>
                    `;
                }

                async function fetchAndRenderEvents(category = '', location = '') {
                    const container = document.getElementById('events-grid-full');
                    if (!container) return;

                    container.innerHTML = `
                        <div class="col-span-full py-16 flex flex-col items-center justify-center text-slate-400 gap-3">
                            <span class="material-symbols-outlined animate-spin text-4xl">sync</span>
                            <p class="font-bold">Loading NGO events...</p>
                        </div>
                    `;

                    try {
                        const params = new URLSearchParams();
                        if (category) params.set('category', category);
                        if (location) params.set('location', location);
                        const query = params.toString();
                        const response = await fetch(`/api/events${query ? `?${query}` : ''}`);
                        const data = await response.json();
                        const events = data.events || [];

                        if (!events.length) {
                            container.innerHTML = `<div class="col-span-full text-center py-16 text-slate-400 font-semibold">No events found for selected filters.</div>`;
                            return;
                        }

                        container.innerHTML = events.map(createEventCard).join('');
                    } catch (error) {
                        console.error(error);
                        container.innerHTML = `<div class="col-span-full text-center py-16 text-red-400 font-bold">Could not load NGO events.</div>`;
                    }
                }

                function createEventCard(eventItem) {
                    const title = translateValue(eventItem.title || 'Community Event', window.currentLanguage);
                    const category = translateValue(eventItem.category || 'General', window.currentLanguage);
                    const location = translateValue(eventItem.location || 'Not specified', window.currentLanguage);
                    const description = translateValue(eventItem.description || 'Details will be shared by organizers.', window.currentLanguage);
                    const startDate = eventItem.start_date || 'TBA';
                    const endDate = eventItem.end_date || 'TBA';
                    const organizer = eventItem.org_name || 'Verified Organization';

                    return `
                        <div class="glass-card premium-shadow rounded-2xl p-6 border border-white/40 flex flex-col gap-4 h-full">
                            <div class="flex items-start justify-between gap-3">
                                <div>
                                    <h3 class="text-lg font-extrabold text-primary leading-snug">${title}</h3>
                                    <p class="text-xs text-slate-400 mt-1">By ${organizer}</p>
                                </div>
                                <span class="px-3 py-1 rounded-lg bg-orange-100 text-orange-700 text-[10px] font-bold uppercase tracking-wider">${category}</span>
                            </div>
                            <p class="text-sm text-on-surface-variant leading-relaxed">${description}</p>
                            <div class="grid grid-cols-1 gap-2 text-xs text-slate-600">
                                <div><b>Location:</b> ${location}</div>
                                <div><b>Start:</b> ${startDate}</div>
                                <div><b>End:</b> ${endDate}</div>
                            </div>
                        </div>
                    `;
                }

                function applyEventsFilter() {
                    const category = (document.getElementById('events-category-filter')?.value || '').trim();
                    const location = (document.getElementById('events-location-filter')?.value || '').trim();
                    fetchAndRenderEvents(category, location);
                }

                function clearEventsFilter() {
                    const categoryInput = document.getElementById('events-category-filter');
                    const locationInput = document.getElementById('events-location-filter');
                    if (categoryInput) categoryInput.value = '';
                    if (locationInput) locationInput.value = '';
                    fetchAndRenderEvents();
                }
        // ---------------- TAB SWITCHING LOGIC ----------------
        function switchTab(tabId) {
            // Hide all views
            document.querySelectorAll('.view-section').forEach(el => {
                el.classList.add('hidden-view');
            });
            
            // Show target
            document.getElementById('view-' + tabId).classList.remove('hidden-view');
            
            // Update active states iteratively for top & side navs
            ['nav-link-top', 'nav-link-side'].forEach(className => {
                document.querySelectorAll('.' + className).forEach(link => {
                    const isTarget = link.getAttribute('data-target') === tabId;
                    
                    if (className === 'nav-link-top') {
                        if (isTarget) {
                            link.classList.add('text-orange-500');
                            link.classList.remove('text-slate-500', 'hover:text-blue-900');
                        } else {
                            link.classList.remove('text-orange-500');
                            link.classList.add('text-slate-500', 'hover:text-blue-900');
                        }
                    } else if (className === 'nav-link-side') {
                        if (isTarget) {
                            link.classList.add('text-blue-900', 'border-r-4', 'border-orange-500', 'bg-orange-50/50');
                            link.classList.remove('text-slate-500', 'hover:text-blue-900', 'hover:bg-blue-50');
                        } else {
                            link.classList.remove('text-blue-900', 'border-r-4', 'border-orange-500', 'bg-orange-50/50');
                            link.classList.add('text-slate-500', 'hover:text-blue-900', 'hover:bg-blue-50');
                        }
                    }
                });
            });

            // Hide footer if inside chat for immersive feel
            const footer = document.getElementById('main-footer');
            if (tabId === 'chat' || tabId === 'applications' || tabId === 'org-profile') {
                footer.style.display = 'none';
            } else {
                footer.style.display = 'grid';
            }

            // Hide badge on views where it overlaps
            const badge = document.getElementById('verified-badge');
            if (badge) {
                if (tabId === 'chat' || tabId === 'schemes') {
                    badge.style.opacity = '0';
                    badge.style.pointerEvents = 'none';
                } else {
                    badge.style.opacity = '1';
                }
            }

            // Scroll to top
            window.scrollTo({ top: 0, behavior: 'smooth' });

            if (tabId === 'events') {
                fetchAndRenderEvents();
            }
        }

        // ---------------- APP STATE ----------------
        window.currentLanguage = 'english';
        window.currentMode = 'citizen';
        window.authToken = localStorage.getItem('sahara_auth_token') || '';
        window.orgAuthToken = localStorage.getItem('sahara_org_auth_token') || '';
        window.currentOrg = null;
        window.currentUser = null;
        window.currentDisplayName = 'Citizen';
        window.lastBotAnswer = '';
        window.botMessageStore = {};
        window.botMessageCounter = 0;
        window.isRecording = false;
        window.isTranscribing = false;
        window.isSpeaking = false;
        window.currentAudio = null;
        window.mediaRecorder = null;
        window.activeStream = null;
        window.speechRecognition = null;
        window.recordingTimeout = null;
        window.recordingMimeType = '';
        window.recordedChunks = [];
        window.__i18nTextNodes = [];
        window.preloaderStartedAt = Date.now();
        window.preloaderHideRequested = false;
        window.preloaderMinMs = 3000;
        window.chatSessionId = localStorage.getItem('sahara_chat_session_id') || '';
        window.isSidebarCollapsed = false;

        const UI_TEXT = {
            english: {
                welcome: "Hello! I am Sahara AI. Please ask me any questions about government schemes or applications and I'll guide you step-by-step.",
                thinking: "Sahara AI is thinking...",
                noSchemes: "No schemes found.",
                schemeLoadError: "Failed to load schemes. Please ensure the server is running.",
                askError: "Sorry, I encountered an error. Please try again.",
                connectionError: "Connection error. Ensure the server is running.",
                startVoice: "Start voice input",
                stopVoice: "Stop recording",
                fillFields: "Please fill in all fields",
                noAnswerToSpeak: "No answer available to speak yet."
            },
            hindi: {
                welcome: "नमस्ते! मैं Sahara AI हूं। सरकारी योजनाओं या आवेदन से जुड़ा कोई भी सवाल पूछिए, मैं चरण-दर-चरण मदद करूंगा।",
                thinking: "Sahara AI सोच रहा है...",
                noSchemes: "कोई योजना नहीं मिली।",
                schemeLoadError: "योजनाएं लोड नहीं हो सकीं। कृपया सर्वर चल रहा है या नहीं, जांचें।",
                askError: "माफ कीजिए, एक त्रुटि आई। कृपया दोबारा प्रयास करें।",
                connectionError: "कनेक्शन त्रुटि। कृपया सुनिश्चित करें कि सर्वर चल रहा है।",
                startVoice: "बोलें",
                stopVoice: "रिकॉर्डिंग रोकें",
                fillFields: "कृपया सभी फील्ड भरें",
                noAnswerToSpeak: "सुनाने के लिए अभी कोई उत्तर नहीं है।"
            },
            hinglish: {
                welcome: "Namaste! Main Sahara AI hoon. Govt schemes ya application se related koi bhi sawaal poochho, main step-by-step help karunga.",
                thinking: "Sahara AI soch raha hai...",
                noSchemes: "Koi scheme nahi mili.",
                schemeLoadError: "Schemes load nahi hui. Please check karo server chal raha hai ya nahi.",
                askError: "Sorry, error aaya. Please dobara try karo.",
                connectionError: "Connection error. Ensure karo ki server chal raha hai.",
                startVoice: "Voice input start karo",
                stopVoice: "Recording stop karo",
                fillFields: "Please sab fields fill karo",
                noAnswerToSpeak: "Sunane ke liye abhi koi answer nahi hai."
            }
        };

        const TEXT_TRANSLATIONS = {
            hindi: {
                "Home": "होम",
                "Schemes": "योजनाएं",
                "Applications": "आवेदन",
                "NGO Events": "एनजीओ इवेंट्स",
                "Profile": "प्रोफाइल",
                "Chat Assistant": "चैट सहायक",
                "Menu": "मेनू",
                "Use side menu to navigate": "नेविगेट करने के लिए साइड मेनू का उपयोग करें",
                "Sign In": "साइन इन",
                "Create Account": "खाता बनाएं",
                "Welcome Back": "फिर से स्वागत है",
                "Namaste,": "नमस्ते,",
                "Search": "खोजें",
                "Tailored for You": "आपके लिए चुना गया",
                "View All Schemes": "सभी योजनाएं देखें",
                "Apply Now": "अभी आवेदन करें",
                "Check Status": "स्थिति जांचें",
                "Benefit Tracker": "लाभ ट्रैकर",
                "Application Success": "आवेदन सफलता",
                "Your Applications": "आपके आवेदन",
                "Status & Tracking": "स्थिति और ट्रैकिंग",
                "Citizen Profile": "नागरिक प्रोफाइल",
                "Personal Details": "व्यक्तिगत विवरण",
                "New Session": "नया सत्र",
                "Assistance Hotlines": "सहायता हेल्पलाइन",
                "Nearby Help (NGOs)": "नजदीकी सहायता (एनजीओ)",
                "Category": "श्रेणी",
                "Location": "स्थान",
                "Eligibility": "पात्रता",
                "No NGOs found.": "कोई एनजीओ नहीं मिला।",
                "Loading NGOs...": "एनजीओ लोड हो रहे हैं...",
                "Error loading NGOs.": "एनजीओ लोड करने में त्रुटि।"
                ,"Aadhaar / Mobile Number": "आधार / मोबाइल नंबर"
                ,"Password / OTP": "पासवर्ड / ओटीपी"
                ,"Full Name": "पूरा नाम"
                ,"State": "राज्य"
                ,"Category": "श्रेणी"
                ,"Password": "पासवर्ड"
                ,"All Schemes Explorer": "सभी योजनाएं एक्सप्लोरर"
                ,"Status": "स्थिति"
                ,"Verified Citizen": "सत्यापित नागरिक"
                ,"Search for schemes, services, or eligibility...": "योजनाएं, सेवाएं या पात्रता खोजें..."
                ,"यहाँ अपना सवाल लिखें...": "यहाँ अपना सवाल लिखें..."
            },
            hinglish: {
                "Home": "Home",
                "Schemes": "Schemes",
                "Applications": "Applications",
                "NGO Events": "NGO Events",
                "Profile": "Profile",
                "Chat Assistant": "Chat Assistant",
                "Menu": "Menu",
                "Use side menu to navigate": "Navigation ke liye side menu use karo",
                "Sign In": "Sign In",
                "Create Account": "Account Banao",
                "Welcome Back": "Welcome Back",
                "Namaste,": "Namaste,",
                "Search": "Search",
                "Tailored for You": "Aapke liye pick kiya gaya",
                "View All Schemes": "Saari Schemes Dekho",
                "Apply Now": "Abhi Apply Karo",
                "Check Status": "Status Check Karo",
                "Benefit Tracker": "Benefit Tracker",
                "Application Success": "Application Success",
                "Your Applications": "Aapke Applications",
                "Status & Tracking": "Status aur Tracking",
                "Citizen Profile": "Citizen Profile",
                "Personal Details": "Personal Details",
                "New Session": "Naya Session",
                "Assistance Hotlines": "Help Hotlines",
                "Nearby Help (NGOs)": "Nearby Help (NGO)",
                "Category": "Category",
                "Location": "Location",
                "Eligibility": "Eligibility",
                "No NGOs found.": "Koi NGO nahi mila.",
                "Loading NGOs...": "NGO load ho rahe hain...",
                "Error loading NGOs.": "NGO load karne mein error."
                ,"Aadhaar / Mobile Number": "Aadhaar / Mobile Number"
                ,"Password / OTP": "Password / OTP"
                ,"Full Name": "Full Name"
                ,"State": "State"
                ,"Category": "Category"
                ,"Password": "Password"
                ,"All Schemes Explorer": "All Schemes Explorer"
                ,"Status": "Status"
                ,"Verified Citizen": "Verified Citizen"
                ,"Search for schemes, services, or eligibility...": "Schemes, services ya eligibility search karo..."
                ,"यहाँ अपना सवाल लिखें...": "Yahan apna sawaal likho..."
            }
        };

        function t(key) {
            return (UI_TEXT[window.currentLanguage] && UI_TEXT[window.currentLanguage][key]) || UI_TEXT.english[key] || key;
        }

        function captureTextNodes() {
            const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
                acceptNode: node => {
                    if (!node.parentElement) return NodeFilter.FILTER_REJECT;
                    const tag = node.parentElement.tagName;
                    if (tag === 'SCRIPT' || tag === 'STYLE') return NodeFilter.FILTER_REJECT;
                    if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
                    return NodeFilter.FILTER_ACCEPT;
                }
            });

            const nodes = [];
            while (walker.nextNode()) {
                nodes.push({ node: walker.currentNode, original: walker.currentNode.nodeValue });
            }
            window.__i18nTextNodes = nodes;

            document.querySelectorAll('input[placeholder]').forEach(input => {
                input.dataset.originalPlaceholder = input.getAttribute('placeholder');
            });
        }

        function translateValue(original, lang) {
            if (lang === 'english') return original;
            const dict = TEXT_TRANSLATIONS[lang] || {};
            const trimmed = (original || '').trim();
            if (!trimmed) return original;
            // Try direct match
            if (dict[trimmed]) return dict[trimmed];
            // Try lowercased match
            if (dict[trimmed.toLowerCase()]) return dict[trimmed.toLowerCase()];
            // Try partial match for common phrases
            for (const key in dict) {
                if (trimmed.includes(key)) {
                    return trimmed.replace(key, dict[key]);
                }
            }
            return original;
        }

        function applyPageLanguage() {
            window.__i18nTextNodes.forEach(item => {
                item.node.nodeValue = translateValue(item.original, window.currentLanguage);
            });

            document.querySelectorAll('input[data-original-placeholder]').forEach(input => {
                const base = input.dataset.originalPlaceholder;
                input.setAttribute('placeholder', translateValue(base, window.currentLanguage));
            });

            const voiceButton = document.getElementById('voice-input-btn');
            if (voiceButton) {
                voiceButton.setAttribute('title', window.isRecording ? t('stopVoice') : t('startVoice'));
            }

            const speakButton = document.getElementById('speak-last-btn');
            if (speakButton) {
                speakButton.setAttribute('title', window.currentLanguage === 'hindi' ? 'आखिरी उत्तर सुनें' : window.currentLanguage === 'hinglish' ? 'Last answer suno' : 'Listen to last answer');
            }

            const langLabel = document.getElementById('lang-label');
            if (langLabel) {
                langLabel.textContent = window.currentLanguage === 'english' ? 'English | हिंदी' : window.currentLanguage === 'hindi' ? 'हिंदी' : 'Hinglish | हिंदी';
            }

            const menuGuide = document.getElementById('menu-guide-text');
            if (menuGuide) {
                menuGuide.textContent = translateValue('Use side menu to navigate', window.currentLanguage);
            }

            // Re-render NGO sections in selected language
            fetchAndRenderNGOs('dashboard-ngo-cards', 3);
                fetchAndRenderNGOs('explore-ngo-cards', 10);
            fetchAndRenderEvents();
        }

        function toggleLanguage() {
            const order = ['english', 'hindi', 'hinglish'];
            const idx = order.indexOf(window.currentLanguage);
            window.currentLanguage = order[(idx + 1) % order.length];
            applyPageLanguage();
        }

        function setSidebarCollapsed(collapsed) {
            const sidebar = document.getElementById('main-sidebar');
            const mainContent = document.getElementById('main-content');
            if (!sidebar || !mainContent) return;
            sidebar.classList.toggle('sidebar-collapsed', collapsed);
            mainContent.classList.toggle('sidebar-collapsed', collapsed);
            window.isSidebarCollapsed = collapsed;
        }

        function toggleSidebar(event) {
            if (event) event.stopPropagation();
            setSidebarCollapsed(!window.isSidebarCollapsed);
        }

        function handleOutsideSidebarClick(event) {
            const sidebar = document.getElementById('main-sidebar');
            if (!sidebar) return;
            if (window.isSidebarCollapsed) return;
            if (!sidebar.contains(event.target)) {
                setSidebarCollapsed(true);
            }
        }

        function updateAuthUI() {
            const isLoggedIn = !!window.authToken;
            const isOrgLoggedIn = !!window.orgAuthToken;
            const guestActions = document.getElementById('guest-auth-actions');
            const userProfileAction = document.getElementById('user-profile-action');
            const verifiedBadge = document.getElementById('verified-badge');
            const orgPanel = document.getElementById('org-admin-panel');
            const orgSubtitle = document.getElementById('org-admin-subtitle');

            if (guestActions) {
                guestActions.style.display = (isLoggedIn || isOrgLoggedIn) ? 'none' : 'flex';
            }

            if (userProfileAction) {
                if (isLoggedIn) {
                    userProfileAction.classList.remove('hidden-view');
                } else {
                    userProfileAction.classList.add('hidden-view');
                }
            }

            if (verifiedBadge) {
                verifiedBadge.style.display = isLoggedIn ? '' : 'none';
            }

            if (orgPanel) {
                if (isOrgLoggedIn) {
                    orgPanel.classList.remove('hidden-view');
                    if (orgSubtitle) {
                        const orgName = (window.currentOrg && window.currentOrg.name) || 'Organization Admin';
                        orgSubtitle.textContent = `Logged in as ${orgName}. Create verified events below.`;
                    }
                } else {
                    orgPanel.classList.add('hidden-view');
                    if (orgSubtitle) {
                        orgSubtitle.textContent = 'Login as organization admin to create events.';
                    }
                }
            }

            // Show/hide org dashboard nav item
            const orgNavItem = document.getElementById('org-nav-item');
            if (orgNavItem) {
                orgNavItem.style.display = isOrgLoggedIn ? '' : 'none';
            }
        }

        function hideAuthOverlay() {
            const authScreen = document.getElementById('auth-screen');
            if (!authScreen) return;
            authScreen.style.opacity = '1';
            authScreen.style.transform = 'scale(1)';
            authScreen.style.display = 'none';
        }

        function openAuth(mode = 'login') {
            const authScreen = document.getElementById('auth-screen');
            if (!authScreen) return;
            authScreen.style.display = 'flex';
            authScreen.style.opacity = '1';
            authScreen.style.transform = 'scale(1)';
            if (mode === 'signup') {
                showSignup();
            } else if (mode === 'org-login') {
                showOrgLogin();
            } else {
                showLogin();
            }
        }

        function hidePreloader() {
            const preloader = document.getElementById('app-preloader');
            if (!preloader || preloader.classList.contains('preloader-hidden')) return;
            preloader.classList.add('preloader-hidden');
            setTimeout(() => {
                if (preloader && preloader.parentNode) preloader.parentNode.removeChild(preloader);
            }, 520);
        }

        function requestHidePreloader() {
            if (window.preloaderHideRequested) return;
            window.preloaderHideRequested = true;

            const elapsed = Date.now() - (window.preloaderStartedAt || Date.now());
            const remaining = Math.max(0, (window.preloaderMinMs || 3000) - elapsed);
            setTimeout(hidePreloader, remaining);
        }

        document.addEventListener("DOMContentLoaded", () => {
            fetchAndRenderSchemes(1);
            fetchAndRenderNGOs('dashboard-ngo-cards', 3);
                fetchAndRenderNGOs('explore-ngo-cards', 10);
            fetchAndRenderEvents();
            captureTextNodes();
            applyPageLanguage();
            appendBotMessage(t('welcome'));
            refreshPersonalizedUI();
            updateAuthUI();
            tryAutoLogin();
            tryAutoOrgLogin();
            setSidebarCollapsed(false);
            document.addEventListener('click', handleOutsideSidebarClick);

            const preloaderVideo = document.getElementById('preloader-video');
            if (preloaderVideo) {
                preloaderVideo.addEventListener('error', () => {
                    requestHidePreloader();
                }, { once: true });
            }
        });

        window.addEventListener('load', () => {
            requestHidePreloader();
        });

        // Safety fallback: if load event is delayed, still remove preloader after minimum display.
        setTimeout(requestHidePreloader, 5000);

        function getAuthHeaders() {
            if (!window.authToken) return {};
            return { 'Authorization': `Bearer ${window.authToken}` };
        }

        function getOrgAuthHeaders() {
            if (!window.orgAuthToken) return {};
            return { 'Authorization': `Bearer ${window.orgAuthToken}` };
        }

        function refreshPersonalizedUI() {
            const name = (window.currentUser && (window.currentUser.full_name || window.currentUser.identifier)) || window.currentDisplayName || 'Citizen';
            window.currentDisplayName = name;

            const heroName = document.getElementById('home-hero-name');
            if (heroName) heroName.textContent = name;

            const miniGreeting = document.getElementById('mini-chat-greeting');
            if (miniGreeting) {
                miniGreeting.textContent = `Hello ${name}! I see your profile is verified. Click anywhere here to enlarge our chat room and ask me any queries!`;
            }
        }

        function applyUserProfile(user) {
            if (!user) return;
            window.currentUser = user;
            const name = user.full_name || user.identifier || 'Citizen';
            window.currentDisplayName = name;
            const profileNameCard = document.getElementById('profile-name-card');
            const profileIdCard = document.getElementById('profile-id-card');
            const profileNameDetail = document.getElementById('profile-name-detail');
            const profileStateDetail = document.getElementById('profile-state-detail');
            const profileCategoryDetail = document.getElementById('profile-category-detail');

            if (profileNameCard) profileNameCard.textContent = name;
            if (profileIdCard) profileIdCard.textContent = `ID: ${user.identifier || 'N/A'}`;
            if (profileNameDetail) profileNameDetail.textContent = name;
            if (profileStateDetail) profileStateDetail.textContent = user.state || 'Not provided';
            if (profileCategoryDetail) profileCategoryDetail.textContent = user.category || 'Not provided';
            refreshPersonalizedUI();
        }

        async function loadBookmarks() {
            const container = document.getElementById('profile-bookmarks');
            if (!container) return;
            if (!window.authToken) {
                container.innerHTML = '<span>Login to see saved schemes.</span>';
                return;
            }

            container.innerHTML = '<span>Loading saved schemes...</span>';
            try {
                const res = await fetch('/api/bookmarks', { headers: getAuthHeaders() });
                const data = await res.json();
                if (!data.ok) {
                    container.innerHTML = '<span>Could not load saved schemes.</span>';
                    return;
                }
                const list = data.bookmarks || [];
                if (!list.length) {
                    container.innerHTML = '<span>No saved schemes yet.</span>';
                    return;
                }
                container.innerHTML = list.map(item => `
                    <div class="flex items-center justify-between p-3 rounded-lg border border-slate-200 bg-slate-50">
                        <span class="font-semibold text-slate-700">${item.scheme_name}</span>
                        <button onclick="removeBookmark(${item.id})" class="text-xs px-3 py-1 rounded-md border border-slate-300 hover:bg-white">Remove</button>
                    </div>
                `).join('');
            } catch (_) {
                container.innerHTML = '<span>Error while loading bookmarks.</span>';
            }
        }

        async function saveBookmark(encodedScheme) {
            if (!window.authToken) {
                showToast('Please login to save schemes.', 'error');
                return;
            }
            try {
                const scheme = JSON.parse(decodeURIComponent(encodedScheme));
                const res = await fetch('/api/bookmarks', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        ...getAuthHeaders()
                    },
                    body: JSON.stringify({ scheme_name: scheme.scheme_name, scheme })
                });
                const data = await res.json();
                if (!data.ok) {
                    showToast(data.message || 'Could not save scheme.', 'error');
                    return;
                }
                showToast('Scheme saved to profile.', 'success');
                loadBookmarks();
            } catch (_) {
                showToast('Failed to save scheme.', 'error');
            }
        }

        async function removeBookmark(bookmarkId) {
            if (!window.authToken) return;
            try {
                const res = await fetch(`/api/bookmarks/${bookmarkId}`, {
                    method: 'DELETE',
                    headers: getAuthHeaders()
                });
                const data = await res.json();
                if (!data.ok) {
                    showToast('Could not remove bookmark.', 'error');
                    return;
                }
                showToast('Bookmark removed.', 'success');
                loadBookmarks();
            } catch (_) {
                showToast('Failed to remove bookmark.', 'error');
            }
        }

        async function tryAutoLogin() {
            if (!window.authToken) return;
            try {
                const res = await fetch('/api/auth/me', { headers: getAuthHeaders() });
                const data = await res.json();
                if (data.ok && data.user) {
                    applyUserProfile(data.user);
                    completeAuth(data.user.full_name || data.user.identifier || 'Citizen');
                    loadBookmarks();
                } else {
                    localStorage.removeItem('sahara_auth_token');
                    window.authToken = '';
                    updateAuthUI();
                }
            } catch (_) {
                localStorage.removeItem('sahara_auth_token');
                window.authToken = '';
                updateAuthUI();
            }
        }

        async function tryAutoOrgLogin() {
            if (!window.orgAuthToken) return;
            try {
                const res = await fetch('/api/org/me', { headers: getOrgAuthHeaders() });
                const data = await res.json();
                if (data.ok && data.org) {
                    window.currentOrg = data.org;
                    updateAuthUI();
                    fillOrgProfileUI(data.org);
                    loadOrgEvents();
                } else {
                    localStorage.removeItem('sahara_org_auth_token');
                    window.orgAuthToken = '';
                    window.currentOrg = null;
                    updateAuthUI();
                }
            } catch (_) {
                localStorage.removeItem('sahara_org_auth_token');
                window.orgAuthToken = '';
                window.currentOrg = null;
                updateAuthUI();
            }
        }

        // ---------------- SCHEMES FETCH LOGIC ----------------

        function getProfileLocation() {
            const u = window.currentUser || {};
            return (u.state || u.location || 'Rajasthan').trim();
        }
        function getProfileCategory() {
            const u = window.currentUser || {};
            return (u.category || '').trim();
        }

        async function fetchAndRenderSchemes(page) {
            const grid = document.getElementById('schemes-grid-full');
            const btn1 = document.getElementById('btn-page-1');
            const btn2 = document.getElementById('btn-page-2');

            // Show loading
            grid.innerHTML = `
                <div class="col-span-full py-20 flex flex-col items-center justify-center text-slate-400 gap-4">
                    <span class="material-symbols-outlined animate-spin text-4xl">sync</span>
                    <p class="font-bold">${window.currentLanguage === 'hindi' ? `आपके लिए योजनाएं लोड हो रही हैं...` : window.currentLanguage === 'hinglish' ? `Aapke liye schemes load ho rahi hain...` : `Loading schemes for you...`}</p>
                </div>
            `;

            // Update button styles
            if (page === 1) {
                if (btn1) btn1.className = "px-6 py-2 rounded-lg text-sm font-bold transition-all bg-primary text-white";
                if (btn2) btn2.className = "px-6 py-2 rounded-lg text-sm font-bold transition-all text-slate-500 hover:bg-slate-50";
            } else {
                if (btn1) btn1.className = "px-6 py-2 rounded-lg text-sm font-bold transition-all text-slate-500 hover:bg-slate-50";
                if (btn2) btn2.className = "px-6 py-2 rounded-lg text-sm font-bold transition-all bg-primary text-white";
            }

            const state = encodeURIComponent(getProfileLocation());
            const category = encodeURIComponent(getProfileCategory());

            try {
                const response = await fetch(`/api/schemes?page=${page}&limit=10&state=${state}&category=${category}`);
                const data = await response.json();

                grid.innerHTML = '';
                if (data.schemes && data.schemes.length > 0) {
                    // Show location context
                    const locLabel = getProfileLocation();
                    grid.innerHTML = `<p class="col-span-full text-sm font-bold text-slate-500 mb-2">
                        📍 Showing schemes relevant to <span class="text-primary">${locLabel}</span> — ${data.schemes.length} of ${data.total} found
                    </p>`;
                    data.schemes.forEach(scheme => {
                        grid.innerHTML += createSchemeCard(scheme);
                    });
                } else {
                    grid.innerHTML = `<p class="col-span-full text-center py-20 text-slate-400">${t('noSchemes')}</p>`;
                }
            } catch (err) {
                console.error(err);
                grid.innerHTML = `<p class="col-span-full text-center py-20 text-red-400 font-bold">${t('schemeLoadError')}</p>`;
            }
        }

        function createSchemeCard(scheme) {
            const icon = scheme.category === 'Agriculture' ? 'agriculture' : 
                         scheme.category === 'Education' ? 'school' : 
                         scheme.category === 'Housing' ? 'home_work' : 'account_balance';
            
            return `
                <div class="glass-card premium-shadow rounded-[2rem] p-8 border border-white/40 flex flex-col gap-6 relative overflow-hidden group h-full transition-transform hover:-translate-y-2">
                    <div class="absolute top-0 right-0 w-32 h-32 bg-secondary-container/10 rounded-bl-full -mr-8 -mt-8"></div>
                    <div class="w-14 h-14 bg-secondary-fixed rounded-2xl flex items-center justify-center text-on-secondary-fixed">
                        <span class="material-symbols-outlined text-3xl" style="font-variation-settings: 'FILL' 1;">${icon}</span>
                    </div>
                    <div class="flex-1">
                        <h3 class="text-xl font-extrabold text-primary mb-2 line-clamp-2">${scheme.scheme_name}</h3>
                        <p class="text-on-surface-variant text-sm leading-relaxed mb-6 line-clamp-3">${scheme.description || 'No description available.'}</p>
                        <div class="flex flex-wrap gap-2 mb-8">
                            <span class="px-3 py-1 bg-green-100 text-green-700 rounded-lg text-[10px] font-bold uppercase tracking-wider">${scheme.level || 'State'}</span>
                            <span class="px-3 py-1 bg-surface-container-high text-on-surface-variant rounded-lg text-[10px] font-bold uppercase tracking-wider">${scheme.category || 'Welfare'}</span>
                        </div>
                    </div>
                    <a href="${scheme.apply_url}" target="_blank" class="w-full py-4 bg-primary text-white rounded-xl font-bold text-sm text-center hover:bg-primary-container transition-all block shadow-lg shadow-primary/10">Apply Now</a>
                    <button onclick="saveBookmark('${encodeURIComponent(JSON.stringify(scheme))}')" class="w-full py-3 mt-2 bg-white text-primary rounded-xl font-bold text-sm text-center border border-slate-200 hover:bg-slate-50 transition-all block">Save Scheme</button>
                </div>
            `;
        }
        // ---------------- RAG CHAT LOGIC ----------------

        function escapeHtml(value) {
            return String(value || '')
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#39;');
        }

        function emphasizeAmounts(rawText) {
            const text = String(rawText || '');
            const amountPattern = /(₹\s?\d[\d,]*(?:\.\d+)?|Rs\.?\s?\d[\d,]*(?:\.\d+)?|INR\s?\d[\d,]*(?:\.\d+)?)/gi;
            return text.replace(amountPattern, '<span class="amount-highlight">$1</span>');
        }

        function parseMarkers(text) {
            let processed = text;

            // --- SCHEME CARDS ---
            // Use [\/\S\s] trick to match across newlines in older browsers too
            processed = processed.replace(/:::SCHEME_CARD([\/\S\s]*?):::/g, (match, content) => {
                const data = {};
                content.trim().split('\n').forEach(line => {
                    const colon = line.indexOf(':');
                    if (colon > 0) {
                        const key = line.slice(0, colon).trim().toLowerCase();
                        const val = line.slice(colon + 1).trim();
                        data[key] = val;
                    }
                });
                const schemeName = (data.name || 'Scheme').replace(/'/g, "&#39;");
                const link = data.link || '#';
                const deadline = data.deadline || 'Apply Soon';
                const benefits = data.benefits || 'N/A';
                // Build amounts inline
                const benefitsHtml = benefits.replace(/(\u20b9\s?\d[\d,]*(?:\.\d+)?|Rs\.?\s?\d[\d,]*(?:\.\d+)?)/gi, '<span class="amount-highlight">$1</span>');

                return `<div class="rich-card scheme-card">
  <div class="rich-card-badge">🏛️ Government Scheme</div>
  <div class="rich-card-title">${data.name || 'Scheme Name'}</div>
  <div class="rich-card-detail"><span class="detail-label">👤 Who can apply:</span><span>${data.who || 'N/A'}</span></div>
  <div class="rich-card-detail"><span class="detail-label">💰 Benefits:</span><span>${benefitsHtml}</span></div>
  <div class="rich-card-detail"><span class="detail-label">📄 Documents:</span><span>${data.documents || 'N/A'}</span></div>
  <div class="rich-card-detail deadline-row"><span class="detail-label">⏰ Deadline:</span><span class="deadline-badge">${deadline}</span></div>
  <div class="rich-card-actions">
    <a href="${link}" target="_blank" rel="noopener noreferrer" class="rich-card-btn btn-primary-card">Apply Now →</a>
    <a href="${link}" target="_blank" rel="noopener noreferrer" class="rich-card-btn btn-secondary-card">View Details</a>
  </div>
</div>`;
            });

            // --- NGO CARDS ---
            processed = processed.replace(/:::NGO_CARD([\/\S\s]*?):::/g, (match, content) => {
                const data = {};
                content.trim().split('\n').forEach(line => {
                    const colon = line.indexOf(':');
                    if (colon > 0) {
                        const key = line.slice(0, colon).trim().toLowerCase();
                        const val = line.slice(colon + 1).trim();
                        data[key] = val;
                    }
                });
                const contact = data.contact || '';
                const contactHtml = contact.startsWith('http')
                    ? `<a href="${contact}" target="_blank" rel="noopener noreferrer">${contact}</a>`
                    : contact;

                return `<div class="rich-card ngo-card">
  <div class="rich-card-badge ngo-badge">🤝 Help Center / NGO</div>
  <div class="rich-card-title ngo-title">${data.name || 'NGO'}</div>
  <div class="rich-card-detail"><span class="detail-label">🆘 Help offered:</span><span>${data.help || 'N/A'}</span></div>
  <div class="rich-card-detail"><span class="detail-label">📍 Location:</span><span>${data.location || 'N/A'}</span></div>
  <div class="rich-card-detail"><span class="detail-label">📞 Contact:</span><span>${contactHtml}</span></div>
</div>`;
            });

            return processed;
        }

        function renderAssistantMarkdown(rawText) {
            const fallback = escapeHtml(rawText).replace(/\n/g, '<br/>');
            if (!window.marked || !window.DOMPurify) return fallback;

            marked.setOptions({
                gfm: true,
                breaks: true,
                headerIds: false,
                mangle: false
            });

            // Parse custom card markers FIRST, before marked.parse()
            // so they arrive as raw HTML and marked doesn't touch them
            const withCards = parseMarkers(rawText);
            const enriched = emphasizeAmounts(withCards);
            const parsed = marked.parse(enriched);
            const safeHtml = DOMPurify.sanitize(parsed, {
                USE_PROFILES: { html: true },
                ADD_TAGS: ['div', 'span', 'a', 'b', 'input'],
                ADD_ATTR: ['target', 'rel', 'class', 'href', 'checked', 'disabled', 'type']
            });

            const container = document.createElement('div');
            container.innerHTML = safeHtml;
            container.querySelectorAll('a').forEach(link => {
                link.setAttribute('target', '_blank');
                link.setAttribute('rel', 'noopener noreferrer');
            });
            container.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
                checkbox.disabled = true;
            });
            return container.innerHTML;
        }
        
        // Append to all boxes so user can see chat in mini view and full view
        function appendUserMessage(text) {
            const boxes = document.querySelectorAll(".chat-message-box");
            boxes.forEach(box => {
                const wrapper = document.createElement("div");
                wrapper.className = "flex flex-col items-end gap-2 my-2 w-full";
                wrapper.innerHTML = `
                    <div class="bg-primary text-white p-4 rounded-2xl rounded-tr-none text-sm leading-relaxed shadow-md w-fit max-w-[90%]">
                        ${escapeHtml(text)}
                    </div>
                `;
                box.appendChild(wrapper);
                box.scrollTop = box.scrollHeight;
            });
        }

        function appendBotMessage(text) {
            window.lastBotAnswer = text;
            window.botMessageCounter += 1;
            const messageId = String(window.botMessageCounter);
            window.botMessageStore[messageId] = text;
            const boxes = document.querySelectorAll(".chat-message-box");
            boxes.forEach(box => {
                const wrapper = document.createElement("div");
                wrapper.className = "flex flex-col gap-2 max-w-[90%] my-2 w-full";
                const renderedMarkdown = renderAssistantMarkdown(text);
                
                wrapper.innerHTML = `
                    <div class="bg-white border border-slate-100 p-5 rounded-2xl rounded-tl-none text-on-surface shadow-sm ai-markdown">
                        ${renderedMarkdown}
                    </div>
                    <button onclick="speakMessageById('${messageId}', this)" class="self-start mt-1 px-3 py-1.5 rounded-lg border border-slate-200 text-slate-500 hover:text-primary hover:bg-slate-50 text-xs font-semibold flex items-center gap-1.5 transition-all" title="Speak this response">
                        <span class="material-symbols-outlined text-sm">volume_up</span>
                        <span>Speak</span>
                    </button>
                `;
                box.appendChild(wrapper);
                box.scrollTop = box.scrollHeight;
            });
        }

        function appendLoading() {
            const boxes = document.querySelectorAll(".chat-message-box");
            boxes.forEach(box => {
                const wrapper = document.createElement("div");
                wrapper.classList.add("loadingIndicator", "flex", "items-center", "gap-2", "p-2", "my-2");
                wrapper.innerHTML = `
                    <span class="material-symbols-outlined animate-spin text-primary">sync</span>
                    <span class="text-xs text-on-surface-variant font-medium">${t('thinking')}</span>
                `;
                box.appendChild(wrapper);
                box.scrollTop = box.scrollHeight;
            });
        }

        function removeLoading() {
            document.querySelectorAll(".loadingIndicator").forEach(el => el.remove());
        }

        async function triggerRAGAPI(queryText) {
            if (!queryText || !queryText.trim()) return;
            
            appendUserMessage(queryText);
            appendLoading();
            
            try {
                // Generate a session ID if not exists
                if (!window.chatSessionId) {
                    window.chatSessionId = "session_" + Math.random().toString(36).substr(2, 9);
                    localStorage.setItem('sahara_chat_session_id', window.chatSessionId);
                }

                const response = await fetch("/api/ask", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        ...getAuthHeaders()
                    },
                    body: JSON.stringify({ 
                        query: queryText, 
                        session_id: window.chatSessionId,
                        language: window.currentLanguage || 'english',
                        mode: window.currentMode || 'citizen'
                    })
                });
                
                const data = await response.json();
                removeLoading();
                
                if (data.answer) {
                    appendBotMessage(data.answer);
                    if (Array.isArray(data.citations) && data.citations.length) {
                        const citationText = data.citations
                            .slice(0, 5)
                            .map(c => `[${c.id}] ${c.source_name} (${c.source_type})`)
                            .join('\n');
                        appendBotMessage(`### Sources\n${citationText}`);
                    }

                    if (Array.isArray(data.follow_up_questions) && data.follow_up_questions.length) {
                        const followText = data.follow_up_questions
                            .map((q, idx) => `${idx + 1}. ${q}`)
                            .join('\n');
                        appendBotMessage(`### To Personalize Better, Please Share\n${followText}`);
                    }

                    if (data.worker_summary) {
                        appendBotMessage(`### Worker Mode Summary\n${String(data.worker_summary)}`);
                    }

                    if (data.understanding_check) {
                        appendBotMessage(`### Confirmation\n${data.understanding_check}`);
                    }
                } else {
                    appendBotMessage(t('askError'));
                }

            } catch (err) {
                console.error(err);
                removeLoading();
                appendBotMessage(t('connectionError'));
            }
        }

        function getRecognitionLang() {
            return window.currentLanguage === 'hindi' ? 'hi-IN' : 'en-IN';
        }

        function updateMicButton(state) {
            const button = document.getElementById('voice-input-btn');
            if (!button) return;
            const icon = button.querySelector('.material-symbols-outlined');

            button.classList.remove('text-red-500', 'border-red-300', 'bg-red-50', 'opacity-60', 'cursor-not-allowed');

            if (state === 'recording') {
                button.classList.add('text-red-500', 'border-red-300', 'bg-red-50');
                if (icon) icon.textContent = 'stop_circle';
                button.setAttribute('title', t('stopVoice'));
                return;
            }

            if (state === 'transcribing') {
                button.classList.add('opacity-60', 'cursor-not-allowed');
                if (icon) icon.textContent = 'sync';
                button.setAttribute('title', window.currentLanguage === 'hindi' ? 'आवाज प्रोसेस हो रही है' : window.currentLanguage === 'hinglish' ? 'Voice process ho rahi hai' : 'Processing voice');
                return;
            }

            if (icon) icon.textContent = 'mic';
            button.setAttribute('title', t('startVoice'));
        }

        function stopActiveMediaTracks() {
            if (window.activeStream) {
                window.activeStream.getTracks().forEach(track => track.stop());
                window.activeStream = null;
            }
        }

        function resetVoiceInputState() {
            window.isRecording = false;
            window.mediaRecorder = null;
            window.speechRecognition = null;
            window.recordedChunks = [];
            window.recordingMimeType = '';
            if (window.recordingTimeout) {
                clearTimeout(window.recordingTimeout);
                window.recordingTimeout = null;
            }
            stopActiveMediaTracks();
            updateMicButton('idle');
        }

        function submitTranscript(transcript) {
            const text = (transcript || '').trim();
            if (!text) {
                appendBotMessage(window.currentLanguage === 'hindi' ? 'आवाज समझ नहीं आई, कृपया दोबारा बोलें।' : window.currentLanguage === 'hinglish' ? 'Voice samajh nahi aayi, please dobara boliye.' : 'Could not understand voice input, please try again.');
                return;
            }

            const input = document.getElementById('actualChatInput');
            if (!input) return;
            input.value = text;
            input.focus();
            triggerRAGAPI(text);
            input.value = '';
        }

        async function startBrowserRecognitionWithFallback() {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {
                await startRecorderCapture();
                return;
            }

            const recognition = new SpeechRecognition();
            window.speechRecognition = recognition;
            recognition.lang = getRecognitionLang();
            recognition.continuous = false;
            recognition.interimResults = true;
            recognition.maxAlternatives = 1;

            let finalTranscript = '';
            let hadAnyResult = false;
            let interimTranscript = '';

            recognition.onresult = (event) => {
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    const result = event.results[i];
                    if (result[0] && result[0].transcript) {
                        hadAnyResult = true;
                        if (result.isFinal) {
                            finalTranscript += ` ${result[0].transcript}`;
                        } else {
                            interimTranscript = result[0].transcript;
                        }
                    }
                }

                // Show live voice transcript in chat input for instant feedback.
                const input = document.getElementById('actualChatInput');
                if (input) {
                    const preview = `${finalTranscript} ${interimTranscript}`.trim();
                    if (preview) input.value = preview;
                }
            };

            recognition.onerror = async () => {
                if (!window.isRecording) return;
                recognition.onend = null;
                try { recognition.stop(); } catch (_) {}
                window.speechRecognition = null;
                await startRecorderCapture();
            };

            recognition.onend = async () => {
                window.speechRecognition = null;
                if (!window.isRecording) return;

                const transcript = `${finalTranscript} ${interimTranscript}`.trim();
                if (transcript) {
                    resetVoiceInputState();
                    submitTranscript(transcript);
                    return;
                }

                if (!hadAnyResult) {
                    await startRecorderCapture();
                    return;
                }

                resetVoiceInputState();
                appendBotMessage(window.currentLanguage === 'hindi' ? 'आवाज समझ नहीं आई, कृपया फिर से कोशिश करें।' : window.currentLanguage === 'hinglish' ? 'Voice clear nahi mili, please dobara try karo.' : 'Could not capture a clear voice input. Please try again.');
            };

            try {
                recognition.start();
            } catch (_) {
                window.speechRecognition = null;
                await startRecorderCapture();
                return;
            }
            window.recordingTimeout = setTimeout(() => {
                if (window.speechRecognition) {
                    try { window.speechRecognition.stop(); } catch (_) {}
                }
            }, 7000);
        }

        async function startRecorderCapture() {
            try {
                if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia || typeof MediaRecorder === 'undefined') {
                    resetVoiceInputState();
                    appendBotMessage(window.currentLanguage === 'hindi' ? 'इस ब्राउज़र में माइक रिकॉर्डिंग सपोर्ट नहीं है।' : window.currentLanguage === 'hinglish' ? 'Is browser mein mic recording support nahi hai.' : 'This browser does not support microphone recording.');
                    return;
                }
                const stream = await navigator.mediaDevices.getUserMedia({
                    audio: {
                        echoCancellation: true,
                        noiseSuppression: true,
                        autoGainControl: true,
                        sampleRate: 16000,
                    },
                });
                window.activeStream = stream;
                window.recordedChunks = [];

                const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
                    ? 'audio/webm;codecs=opus'
                    : MediaRecorder.isTypeSupported('audio/ogg;codecs=opus')
                        ? 'audio/ogg;codecs=opus'
                        : MediaRecorder.isTypeSupported('audio/webm')
                            ? 'audio/webm'
                            : MediaRecorder.isTypeSupported('audio/ogg')
                                ? 'audio/ogg'
                                : '';

                window.mediaRecorder = mimeType ? new MediaRecorder(stream, { mimeType }) : new MediaRecorder(stream);
                window.recordingMimeType = window.mediaRecorder.mimeType || mimeType || 'audio/webm';

                window.mediaRecorder.ondataavailable = event => {
                    if (event.data && event.data.size > 0) {
                        window.recordedChunks.push(event.data);
                    }
                };

                window.mediaRecorder.onstop = async () => {
                    stopActiveMediaTracks();
                    await sendAudioForTranscription();
                };

                window.mediaRecorder.start(250);
                window.recordingTimeout = setTimeout(() => {
                    if (window.mediaRecorder && window.mediaRecorder.state === 'recording') {
                        window.mediaRecorder.stop();
                    }
                }, 8000);
            } catch (error) {
                console.error(error);
                resetVoiceInputState();
                appendBotMessage(window.currentLanguage === 'hindi' ? 'माइक एक्सेस नहीं मिला।' : window.currentLanguage === 'hinglish' ? 'Mic access nahi mila.' : 'Microphone access not available.');
            }
        }

        async function startVoiceInput() {
            if (window.isTranscribing) return;

            if (window.isRecording) {
                if (window.speechRecognition) {
                    try { window.speechRecognition.stop(); } catch (_) {}
                }
                if (window.mediaRecorder && window.mediaRecorder.state === 'recording') {
                    window.mediaRecorder.stop();
                } else {
                    resetVoiceInputState();
                }
                return;
            }

            window.isRecording = true;
            updateMicButton('recording');
            await startBrowserRecognitionWithFallback();
        }

        async function sendAudioForTranscription() {
            if (!window.recordedChunks || window.recordedChunks.length === 0) {
                resetVoiceInputState();
                appendBotMessage(window.currentLanguage === 'hindi' ? 'कोई ऑडियो रिकॉर्ड नहीं हुआ।' : window.currentLanguage === 'hinglish' ? 'Audio record nahi hua.' : 'No audio was captured.');
                return;
            }

            window.isTranscribing = true;
            updateMicButton('transcribing');

            try {
                const detectedType = window.recordingMimeType || (window.recordedChunks[0] && window.recordedChunks[0].type) || 'audio/webm';
                const audioBlob = new Blob(window.recordedChunks, { type: detectedType });
                const formData = new FormData();
                const ext = detectedType.includes('ogg') ? 'ogg' : detectedType.includes('wav') ? 'wav' : 'webm';
                formData.append('audio', audioBlob, `voice.${ext}`);

                const response = await fetch(`/api/stt?language=${window.currentLanguage}`, {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();
                if (data.error === 'ffmpeg-not-found') {
                    appendBotMessage(window.currentLanguage === 'hindi' ? 'आवाज सेवा उपलब्ध नहीं है। ffmpeg कॉन्फ़िगरेशन आवश्यक है।' : window.currentLanguage === 'hinglish' ? 'Voice service abhi available nahi hai. ffmpeg setup zaroori hai.' : 'Voice service is unavailable. ffmpeg setup is required.');
                    return;
                }

                if (data.error) {
                    appendBotMessage(window.currentLanguage === 'hindi' ? 'वॉइस ट्रांसक्रिप्शन में समस्या आई, कृपया दोबारा कोशिश करें।' : window.currentLanguage === 'hinglish' ? 'Voice transcription mein issue aaya, please dobara try karo.' : 'Voice transcription failed. Please try again.');
                    return;
                }

                submitTranscript(data.text || '');
            } catch (error) {
                console.error(error);
                appendBotMessage(t('connectionError'));
            } finally {
                window.isTranscribing = false;
                resetVoiceInputState();
            }
        }

        async function speakLastAnswer() {
            if (!window.lastBotAnswer || !window.lastBotAnswer.trim()) {
                showToast(t('noAnswerToSpeak'), 'info');
                return;
            }

            await playTTS(window.lastBotAnswer, document.getElementById('speak-last-btn'));
        }
        // ---------------- AUTH LOGIC ----------------
        function showSignup() {
            document.getElementById('login-form').style.display = 'none';
            document.getElementById('org-login-form').style.display = 'none';
            document.getElementById('signup-form').style.display = 'block';
        }
        function showLogin() {
            document.getElementById('signup-form').style.display = 'none';
            document.getElementById('org-login-form').style.display = 'none';
            document.getElementById('login-form').style.display = 'block';
        }
        function showOrgLogin() {
            document.getElementById('signup-form').style.display = 'none';
            document.getElementById('login-form').style.display = 'none';
            document.getElementById('org-login-form').style.display = 'block';
        }
        async function handleLogin() {
            const email = document.getElementById('login-id').value.trim();
            const pass = document.getElementById('login-pass').value;
            if (!email || !pass) { showToast(t('fillFields'), 'error'); return; }
            try {
                const res = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: email, password: pass })
                });
                const data = await res.json();
                if (!data.ok) {
                    showToast(data.message || 'Login failed', 'error');
                    return;
                }
                window.authToken = data.token || '';
                if (window.authToken) {
                    localStorage.setItem('sahara_auth_token', window.authToken);
                }
                applyUserProfile(data.user || {});
                completeAuth((data.user && data.user.full_name) || email);
                loadBookmarks();
                showToast('Login successful.', 'success');
            } catch (e) {
                showToast('Login error. Please try again.', 'error');
            }
        }
        function checkPasswordStrength(val) {
            const bars = [1,2,3,4].map(i => document.getElementById('ps-bar-'+i));
            const hint = document.getElementById('ps-hint');
            if (!hint) return;
            let score = 0;
            if (val.length >= 8) score++;
            if (/[A-Z]/.test(val)) score++;
            if (/[0-9]/.test(val)) score++;
            if (/[^A-Za-z0-9]/.test(val)) score++;
            const colors = ['bg-red-400', 'bg-orange-400', 'bg-yellow-400', 'bg-green-400'];
            const labels = ['Too weak', 'Weak', 'Good', 'Strong ✓'];
            bars.forEach((b, i) => {
                b.className = 'h-1 flex-1 rounded-full transition-all duration-300 ' + (i < score ? colors[score-1] : 'bg-white/20');
            });
            hint.textContent = score === 0 ? 'Min 8 chars · uppercase · number · special char' : labels[score-1];
        }
        async function handleSignup() {
            const name = document.getElementById('signup-name').value.trim();
            const email = document.getElementById('signup-email').value.trim();
            const pass = document.getElementById('signup-pass').value;
            const state = document.getElementById('signup-state').value || '';
            const category = document.getElementById('signup-category').value || '';
            if (!name || !email || !pass) { showToast(t('fillFields'), 'error'); return; }
            // Strong password enforcement
            if (pass.length < 8) { showToast('Password must be at least 8 characters.', 'error'); return; }
            if (!/[A-Z]/.test(pass)) { showToast('Password needs at least one uppercase letter.', 'error'); return; }
            if (!/[0-9]/.test(pass)) { showToast('Password needs at least one number.', 'error'); return; }
            if (!/[^A-Za-z0-9]/.test(pass)) { showToast('Password needs at least one special character.', 'error'); return; }
            try {
                const signupRes = await fetch('/api/auth/signup', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ full_name: name, email: email, password: pass, state, category })
                });
                const signupData = await signupRes.json();
                if (!signupData.ok) {
                    showToast(signupData.message || 'Signup failed', 'error');
                    return;
                }

                const loginRes = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: email, password: pass })
                });
                const loginData = await loginRes.json();
                if (!loginData.ok) {
                    showToast('Account created! Please login.', 'info');
                    showLogin();
                    return;
                }

                window.authToken = loginData.token || '';
                if (window.authToken) {
                    localStorage.setItem('sahara_auth_token', window.authToken);
                }
                applyUserProfile(loginData.user || {});
                completeAuth((loginData.user && loginData.user.full_name) || name);
                loadBookmarks();
                showToast('Account created successfully!', 'success');
            } catch (e) {
                showToast('Signup error. Please try again.', 'error');
            }
        }
        async function handleOrgLogin() {
            const email = document.getElementById('org-login-email').value;
            const pass = document.getElementById('org-login-pass').value;
            if (!email || !pass) { showToast(t('fillFields'), 'error'); return; }

            try {
                const res = await fetch('/api/org/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password: pass })
                });
                const data = await res.json();
                if (!data.ok) {
                    showToast(data.message || 'Organization login failed', 'error');
                    return;
                }
                window.orgAuthToken = data.token || '';
                window.currentOrg = data.org || null;
                if (window.orgAuthToken) {
                    localStorage.setItem('sahara_org_auth_token', window.orgAuthToken);
                }
                showToast('Organization admin login successful.', 'success');
                // Sync org to ngo_data.csv
                try {
                    await fetch('/api/org/sync-csv', { method: 'POST', headers: getOrgAuthHeaders() });
                } catch(_) {}
                hideAuthOverlay();
                updateAuthUI();
                fillOrgProfileUI(data.org || {});
                loadOrgEvents();
                switchTab('org-profile');
            } catch (_) {
                showToast('Organization login error. Please try again.', 'error');
            }
        }

        async function createOrgEvent() {
            if (!window.orgAuthToken) {
                showToast('Please login as organization admin first.', 'error');
                openAuth('org-login');
                return;
            }

            const payload = {
                title: (document.getElementById('event-title').value || '').trim(),
                description: (document.getElementById('event-description').value || '').trim(),
                category: (document.getElementById('event-category').value || '').trim(),
                location: (document.getElementById('event-location').value || '').trim(),
                start_date: (document.getElementById('event-start').value || '').trim(),
                end_date: (document.getElementById('event-end').value || '').trim(),
            };

            if (!payload.title || !payload.description || !payload.location) {
                showToast('Please fill title, description, and location.', 'error');
                return;
            }

            try {
                const res = await fetch('/api/events', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        ...getOrgAuthHeaders()
                    },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (!data.ok) {
                    showToast(data.message || 'Could not create event.', 'error');
                    return;
                }
                showToast('Event created successfully.', 'success');
                ['event-title', 'event-description', 'event-category', 'event-location', 'event-start', 'event-end'].forEach(id => {
                    const el = document.getElementById(id);
                    if (el) el.value = '';
                });
                fetchAndRenderNGOs('dashboard-ngo-cards', 3);
                    fetchAndRenderNGOs('explore-ngo-cards', 10);
                fetchAndRenderEvents();
            } catch (_) {
                showToast('Event creation failed.', 'error');
            }
        }

        function completeAuth(userName) {
            if (userName) {
                window.currentDisplayName = userName;
            }
            const authScreen = document.getElementById('auth-screen');
            const targetTab = window.orgAuthToken ? 'org-profile' : 'profile';
            if (authScreen && authScreen.style.display !== 'none') {
                authScreen.style.transition = 'opacity 0.5s, transform 0.5s';
                authScreen.style.opacity = '0';
                authScreen.style.transform = 'scale(1.05)';
                setTimeout(() => {
                    authScreen.style.display = 'none';
                    authScreen.style.opacity = '1';
                    authScreen.style.transform = 'scale(1)';
                    updateAuthUI();
                    refreshPersonalizedUI();
                    switchTab(targetTab);
                }, 500);
                return;
            }

            updateAuthUI();
            refreshPersonalizedUI();
            switchTab(targetTab);
        }

        // ── ORG PROFILE FUNCTIONS ──────────────────────────────────────────
        function fillOrgProfileUI(org) {
            const set = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val || '—'; };
            set('org-profile-name', org.name);
            set('org-profile-email', org.email);
            set('org-detail-name', org.name);
            set('org-detail-category', org.category);
            set('org-detail-location', org.location);
            set('org-detail-email', org.email);
        }

        async function loadOrgEvents() {
            if (!window.orgAuthToken) return;
            const list = document.getElementById('org-events-list');
            if (list) list.innerHTML = '<p class="text-slate-400 text-sm">Loading...</p>';
            try {
                const res = await fetch('/api/org/my-events', { headers: getOrgAuthHeaders() });
                const data = await res.json();
                if (!data.ok || !data.events || data.events.length === 0) {
                    if (list) list.innerHTML = '<p class="text-slate-400 text-sm">No events yet. Click "Create Event" to add your first event!</p>';
                    return;
                }
                if (list) {
                    list.innerHTML = data.events.map(ev => `
                        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-4 rounded-2xl border border-slate-100 hover:border-blue-200 hover:bg-blue-50/30 transition-all">
                            <div class="flex items-start gap-4">
                                <div class="w-10 h-10 rounded-xl bg-orange-100 flex items-center justify-center flex-shrink-0">
                                    <span class="material-symbols-outlined text-orange-500" style="font-size:20px;font-variation-settings:'FILL' 1;">event</span>
                                </div>
                                <div>
                                    <p class="font-bold text-primary">${ev.title}</p>
                                    <p class="text-sm text-slate-500 mt-0.5">${ev.description}</p>
                                    <div class="flex items-center gap-3 mt-1.5">
                                        ${ev.location ? `<span class="text-xs text-slate-400 flex items-center gap-1"><span class="material-symbols-outlined" style="font-size:13px;">location_on</span>${ev.location}</span>` : ''}
                                        ${ev.start_date ? `<span class="text-xs text-slate-400 flex items-center gap-1"><span class="material-symbols-outlined" style="font-size:13px;">calendar_today</span>${ev.start_date}${ev.end_date ? ' → ' + ev.end_date : ''}</span>` : ''}
                                        ${ev.category ? `<span class="text-xs px-2 py-0.5 bg-orange-50 text-orange-600 rounded-full font-bold">${ev.category}</span>` : ''}
                                    </div>
                                </div>
                            </div>
                            <span class="text-xs px-3 py-1 rounded-full font-bold ${ev.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-slate-100 text-slate-500'}">${ev.status || 'active'}</span>
                        </div>
                    `).join('');
                }
            } catch(e) {
                if (list) list.innerHTML = '<p class="text-red-400 text-sm">Could not load events.</p>';
            }
        }

        function openCreateEventModal() {
            if (!window.orgAuthToken) {
                showToast('Please login as organization admin first.', 'error');
                openAuth('org-login');
                return;
            }
            const modal = document.getElementById('create-event-modal');
            if (modal) modal.style.display = 'flex';
            // Clear form
            ['modal-event-title','modal-event-description','modal-event-location','modal-event-start','modal-event-end'].forEach(id => {
                const el = document.getElementById(id); if (el) el.value = '';
            });
        }

        function closeCreateEventModal() {
            const modal = document.getElementById('create-event-modal');
            if (modal) modal.style.display = 'none';
        }

        async function submitCreateEvent() {
            if (!window.orgAuthToken) {
                showToast('Please login as organization admin first.', 'error');
                return;
            }
            const payload = {
                title: (document.getElementById('modal-event-title').value || '').trim(),
                description: (document.getElementById('modal-event-description').value || '').trim(),
                location: (document.getElementById('modal-event-location').value || '').trim(),
                start_date: (document.getElementById('modal-event-start').value || '').trim(),
                end_date: (document.getElementById('modal-event-end').value || '').trim(),
            };
            if (!payload.title || !payload.description || !payload.location) {
                showToast('Please fill in Event Name, Description, and Location.', 'error');
                return;
            }
            const btn = document.getElementById('modal-submit-btn');
            if (btn) { btn.disabled = true; btn.textContent = 'Saving...'; }
            try {
                const res = await fetch('/api/events', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', ...getOrgAuthHeaders() },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (!data.ok) {
                    showToast(data.message || 'Could not create event.', 'error');
                    return;
                }
                showToast('Event created and saved to CSV!', 'success');
                closeCreateEventModal();
                loadOrgEvents();
                fetchAndRenderNGOs && fetchAndRenderNGOs('dashboard-ngo-cards', 3);
                fetchAndRenderEvents && fetchAndRenderEvents();
            } catch(_) {
                showToast('Event creation failed. Please try again.', 'error');
            } finally {
                if (btn) {
                    btn.disabled = false;
                    btn.innerHTML = '<span class="material-symbols-outlined text-lg">add_circle</span> Create Event';
                }
            }
        }

        function orgLogout() {
            window.orgAuthToken = '';
            window.currentOrg = null;
            localStorage.removeItem('sahara_org_auth_token');
            updateAuthUI();
            switchTab('home');
            showToast('Organization logged out.', 'info');
        }
    </script>
</body>
</html>
"""
