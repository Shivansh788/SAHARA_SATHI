import json

html_content = """<!DOCTYPE html>
<html class="light" lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Sahara Saathi | Empathetic Welfare Dashboard</title>
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
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
                        <label class="text-blue-200 text-xs font-bold uppercase tracking-widest mb-2 block font-['Plus_Jakarta_Sans']">Aadhaar / Mobile Number</label>
                        <input id="login-id" type="text" placeholder="Enter Aadhaar or mobile number" class="w-full h-14 px-5 bg-white/10 border border-white/20 rounded-xl text-white placeholder:text-blue-300/50 focus:outline-none focus:ring-2 focus:ring-orange-400/50 focus:border-orange-400/50 text-sm font-['Plus_Jakarta_Sans']"/>
                    </div>
                    <div>
                        <label class="text-blue-200 text-xs font-bold uppercase tracking-widest mb-2 block font-['Plus_Jakarta_Sans']">Password / OTP</label>
                        <input id="login-pass" type="password" placeholder="Enter password or OTP" class="w-full h-14 px-5 bg-white/10 border border-white/20 rounded-xl text-white placeholder:text-blue-300/50 focus:outline-none focus:ring-2 focus:ring-orange-400/50 focus:border-orange-400/50 text-sm font-['Plus_Jakarta_Sans']"/>
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
                        <label class="text-blue-200 text-xs font-bold uppercase tracking-widest mb-2 block font-['Plus_Jakarta_Sans']">Aadhaar / Mobile Number</label>
                        <input id="signup-id" type="text" placeholder="Enter Aadhaar or mobile number" class="w-full h-14 px-5 bg-white/10 border border-white/20 rounded-xl text-white placeholder:text-blue-300/50 focus:outline-none focus:ring-2 focus:ring-orange-400/50 text-sm font-['Plus_Jakarta_Sans']"/>
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
                        <input id="signup-pass" type="password" placeholder="Create a password" class="w-full h-14 px-5 bg-white/10 border border-white/20 rounded-xl text-white placeholder:text-blue-300/50 focus:outline-none focus:ring-2 focus:ring-orange-400/50 text-sm font-['Plus_Jakarta_Sans']"/>
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
        <div class="px-6 flex flex-col gap-3 flex-1">
            <button onclick="toggleSideMenu()" class="w-full flex items-center justify-between px-4 py-3 rounded-xl bg-white border border-slate-200 text-primary font-bold">
                <span class="flex items-center gap-2">
                    <span class="material-symbols-outlined">menu</span>
                    <span id="side-menu-label" class="font-['Plus_Jakarta_Sans'] text-sm">Menu</span>
                </span>
                <span id="side-menu-chevron" class="material-symbols-outlined">expand_more</span>
            </button>
            <div id="side-menu-items" class="hidden-view flex-col gap-1">
                <a class="nav-link-side cursor-pointer flex items-center gap-4 px-4 py-3 rounded-xl text-blue-900 font-bold border-r-4 border-orange-500 bg-orange-50/50 transition-all duration-300" onclick="switchTab('home')" data-target="home">
                    <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">home</span>
                    <span class="font-['Plus_Jakarta_Sans'] text-sm">Home</span>
                </a>
                <a class="nav-link-side cursor-pointer flex items-center gap-4 px-4 py-3 rounded-xl text-slate-500 hover:text-blue-900 hover:bg-blue-50 transition-all duration-300" onclick="switchTab('schemes')" data-target="schemes">
                    <span class="material-symbols-outlined">account_balance</span>
                    <span class="font-['Plus_Jakarta_Sans'] text-sm">Schemes</span>
                </a>
                <a class="nav-link-side cursor-pointer flex items-center gap-4 px-4 py-3 rounded-xl text-slate-500 hover:text-blue-900 hover:bg-blue-50 transition-all duration-300" onclick="switchTab('applications')" data-target="applications">
                    <span class="material-symbols-outlined">description</span>
                    <span class="font-['Plus_Jakarta_Sans'] text-sm">Applications</span>
                </a>
                <a class="nav-link-side cursor-pointer flex items-center gap-4 px-4 py-3 rounded-xl text-slate-500 hover:text-blue-900 hover:bg-blue-50 transition-all duration-300" onclick="switchTab('chat')" data-target="chat">
                    <span class="material-symbols-outlined">forum</span>
                    <span class="font-['Plus_Jakarta_Sans'] text-sm">Chat Assistant</span>
                </a>
                <a class="nav-link-side cursor-pointer flex items-center gap-4 px-4 py-3 rounded-xl text-slate-500 hover:text-blue-900 hover:bg-blue-50 transition-all duration-300" onclick="switchTab('profile')" data-target="profile">
                    <span class="material-symbols-outlined">person</span>
                    <span class="font-['Plus_Jakarta_Sans'] text-sm">Profile</span>
                </a>
            </div>
        </div>
        <div class="px-8 mt-auto">
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

            <!-- ================= VIEW: CHAT ASSISTANT ================= -->
            <div id="view-chat" class="view-section hidden-view flex flex-col h-[calc(100vh-140px)]">
                <div class="flex-1 bg-surface-container-lowest rounded-[2.5rem] premium-shadow border border-slate-100 flex flex-col overflow-hidden">
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
                    <div class="p-6 bg-white border-t border-slate-100 shadow-[0_-10px_40px_rgba(0,0,0,0.03)] focus-within:bg-blue-50/30 transition-colors">
                        <div class="relative flex items-center gap-4">
                            <button id="voice-input-btn" onclick="startVoiceInput()" class="w-12 h-12 rounded-full border border-slate-200 text-slate-400 hover:text-primary hover:bg-slate-50 flex items-center justify-center transition-all" title="बोलें">
                                <span class="material-symbols-outlined">mic</span>
                            </button>
                            <button id="speak-last-btn" onclick="speakLastAnswer()" class="w-12 h-12 rounded-full border border-slate-200 text-slate-400 hover:text-primary hover:bg-slate-50 flex items-center justify-center transition-all" title="Listen to last answer">
                                <span class="material-symbols-outlined">volume_up</span>
                            </button>
                            <input id="actualChatInput" class="chat-input-field flex-1 h-14 pl-6 pr-16 bg-white rounded-2xl border border-slate-200 outline-none focus:border-primary/50 focus:ring-4 focus:ring-primary/10 text-base shadow-sm font-label transition-all" placeholder="यहाँ अपना सवाल लिखें..." type="text" onkeypress="if(event.key === 'Enter') { triggerRAGAPI(this.value); this.value=''; }"/>
                            <select id="chat-mode-select" class="h-14 px-3 rounded-xl border border-slate-200 text-sm font-semibold text-slate-700 bg-white" onchange="window.currentMode = this.value">
                                <option value="citizen">Citizen</option>
                                <option value="worker">Worker</option>
                                <option value="explorer">Explorer</option>
                            </select>
                            <button onclick="triggerRAGAPI(document.getElementById('actualChatInput').value); document.getElementById('actualChatInput').value='';" class="absolute right-3 top-3 bottom-3 w-10 bg-primary rounded-xl text-white flex items-center justify-center hover:bg-primary-container hover:scale-105 transition-all shadow-md">
                                <span class="material-symbols-outlined text-lg">send</span>
                            </button>
                        </div>
                        <div class="flex justify-center mt-4 text-xs text-slate-400 gap-6">
                            <span class="flex items-center gap-1"><span class="material-symbols-outlined text-[14px]">lock</span> Encrypted specific to your profile</span>
                            <span class="flex items-center gap-1 cursor-pointer hover:text-primary"><span class="material-symbols-outlined text-[14px]">mic</span> English / हिंदी Voice input</span>
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
                async function fetchAndRenderNGOs(targetId, limit = 6) {
                    const container = document.getElementById(targetId);
                    if (!container) return;
                    container.innerHTML = `<span class='text-slate-400'>${window.currentLanguage === 'hindi' ? 'एनजीओ लोड हो रहे हैं...' : window.currentLanguage === 'hinglish' ? 'NGO load ho rahe hain...' : 'Loading NGOs...'}</span>`;
                    try {
                        const response = await fetch('/api/ngos');
                        const data = await response.json();
                        let ngos = data.ngos || [];
                        if (limit) ngos = ngos.slice(0, limit);
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
            if (tabId === 'chat' || tabId === 'applications') {
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

            const menuLabel = document.getElementById('side-menu-label');
            if (menuLabel) {
                menuLabel.textContent = translateValue('Menu', window.currentLanguage);
            }

            const menuGuide = document.getElementById('menu-guide-text');
            if (menuGuide) {
                menuGuide.textContent = translateValue('Use side menu to navigate', window.currentLanguage);
            }

            // Re-render NGO sections in selected language
            fetchAndRenderNGOs('dashboard-ngo-cards', 3);
            fetchAndRenderNGOs('explore-ngo-cards', 0);
        }

        function toggleLanguage() {
            const order = ['english', 'hindi', 'hinglish'];
            const idx = order.indexOf(window.currentLanguage);
            window.currentLanguage = order[(idx + 1) % order.length];
            applyPageLanguage();
        }

        function toggleSideMenu() {
            const menu = document.getElementById('side-menu-items');
            const icon = document.getElementById('side-menu-chevron');
            if (!menu || !icon) return;
            const isHidden = menu.classList.contains('hidden-view');
            if (isHidden) {
                menu.classList.remove('hidden-view');
                menu.classList.add('flex');
                icon.textContent = 'expand_less';
            } else {
                menu.classList.add('hidden-view');
                menu.classList.remove('flex');
                icon.textContent = 'expand_more';
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
                guestActions.style.display = isLoggedIn ? 'none' : 'flex';
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
            fetchAndRenderNGOs('explore-ngo-cards', 0);
            captureTextNodes();
            applyPageLanguage();
            appendBotMessage(t('welcome'));
            refreshPersonalizedUI();
            updateAuthUI();
            tryAutoLogin();
            tryAutoOrgLogin();

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
        
        async function fetchAndRenderSchemes(page) {
            const grid = document.getElementById('schemes-grid-full');
            const btn1 = document.getElementById('btn-page-1');
            const btn2 = document.getElementById('btn-page-2');
            
            // Show loading
            grid.innerHTML = `
                <div class="col-span-full py-20 flex flex-col items-center justify-center text-slate-400 gap-4">
                    <span class="material-symbols-outlined animate-spin text-4xl">sync</span>
                    <p class="font-bold">${window.currentLanguage === 'hindi' ? `पेज ${page} की योजनाएं लोड हो रही हैं...` : window.currentLanguage === 'hinglish' ? `Page ${page} ki schemes load ho rahi hain...` : `Fetching schemes for Page ${page}...`}</p>
                </div>
            `;
            
            // Update button styles
            if(page === 1) {
                btn1.className = "px-6 py-2 rounded-lg text-sm font-bold transition-all bg-primary text-white";
                btn2.className = "px-6 py-2 rounded-lg text-sm font-bold transition-all text-slate-500 hover:bg-slate-50";
            } else {
                btn1.className = "px-6 py-2 rounded-lg text-sm font-bold transition-all text-slate-500 hover:bg-slate-50";
                btn2.className = "px-6 py-2 rounded-lg text-sm font-bold transition-all bg-primary text-white";
            }

            try {
                const response = await fetch(`/api/schemes?page=${page}&limit=50`);
                const data = await response.json();
                
                grid.innerHTML = '';
                if(data.schemes && data.schemes.length > 0) {
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
        
        // Append to all boxes so user can see chat in mini view and full view
        function appendUserMessage(text) {
            const boxes = document.querySelectorAll(".chat-message-box");
            boxes.forEach(box => {
                const wrapper = document.createElement("div");
                wrapper.className = "flex flex-col items-end gap-2 my-2 w-full";
                wrapper.innerHTML = `
                    <div class="bg-primary text-white p-4 rounded-2xl rounded-tr-none text-sm leading-relaxed shadow-md w-fit max-w-[90%]">
                        ${text}
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
                
                // Format markdown numbering and newlines
                const formattedText = text.replace(/\\n/g, "<br/>").replace(/(\\d+\\.)/g, "<strong>$1</strong>");
                
                wrapper.innerHTML = `
                    <div class="bg-white border border-slate-100 p-4 rounded-2xl rounded-tl-none text-sm text-on-surface leading-relaxed shadow-sm">
                        ${formattedText}
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
                            .join('<br/>');
                        appendBotMessage(`<b>Sources</b><br/>${citationText}`);
                    }

                    if (Array.isArray(data.follow_up_questions) && data.follow_up_questions.length) {
                        const followText = data.follow_up_questions
                            .map((q, idx) => `${idx + 1}. ${q}`)
                            .join('<br/>');
                        appendBotMessage(`<b>To personalize better, please share:</b><br/>${followText}`);
                    }

                    if (data.worker_summary) {
                        appendBotMessage(`<b>Worker Mode Summary</b><br/>${String(data.worker_summary).replace(/\\n/g, '<br/>')}`);
                    }

                    if (data.understanding_check) {
                        appendBotMessage(`<b>Confirmation</b><br/>${data.understanding_check}`);
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
            const id = document.getElementById('login-id').value;
            const pass = document.getElementById('login-pass').value;
            if (!id || !pass) { showToast(t('fillFields'), 'error'); return; }
            try {
                const res = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ identifier: id, password: pass })
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
                completeAuth((data.user && data.user.full_name) || id);
                loadBookmarks();
                showToast('Login successful.', 'success');
            } catch (e) {
                showToast('Login error. Please try again.', 'error');
            }
        }
        async function handleSignup() {
            const name = document.getElementById('signup-name').value;
            const id = document.getElementById('signup-id').value;
            const pass = document.getElementById('signup-pass').value;
            const state = document.getElementById('signup-state').value || '';
            const category = document.getElementById('signup-category').value || '';
            if (!name || !id || !pass) { showToast(t('fillFields'), 'error'); return; }
            try {
                const signupRes = await fetch('/api/auth/signup', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ full_name: name, identifier: id, password: pass, state, category })
                });
                const signupData = await signupRes.json();
                if (!signupData.ok) {
                    showToast(signupData.message || 'Signup failed', 'error');
                    return;
                }

                const loginRes = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ identifier: id, password: pass })
                });
                const loginData = await loginRes.json();
                if (!loginData.ok) {
                    showToast('Signup done, please login once.', 'info');
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
                showToast('Signup successful.', 'success');
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
                completeAuth((window.currentUser && window.currentUser.full_name) || 'Citizen');
                updateAuthUI();
                switchTab('profile');
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
                fetchAndRenderNGOs('explore-ngo-cards', 0);
            } catch (_) {
                showToast('Event creation failed.', 'error');
            }
        }

        function completeAuth(userName) {
            if (userName) {
                window.currentDisplayName = userName;
            }
            const authScreen = document.getElementById('auth-screen');
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
                    switchTab('home');
                }, 500);
                return;
            }

            updateAuthUI();
            refreshPersonalizedUI();
            switchTab('home');
        }
    </script>
</body>
</html>
"""
