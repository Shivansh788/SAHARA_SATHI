import json

html_content = """<!DOCTYPE html>
<html class="light" lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Sahara Saathi | Empathetic Welfare Dashboard</title>
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@200;300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet"/>
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
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
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
            display: inline-block;
            line-height: 1;
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
    </style>
</head>
<body class="bg-background text-on-surface min-h-screen">
    <!-- Top Navigation Shell -->
    <header class="fixed top-0 w-full z-50 bg-white/70 backdrop-blur-xl shadow-sm shadow-blue-900/5 px-8 py-4 flex justify-between items-center">
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-primary-container rounded-lg flex items-center justify-center text-white">
                <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">account_balance</span>
            </div>
            <span class="text-2xl font-black text-blue-900 font-['Manrope'] tracking-tight cursor-pointer" onclick="switchTab('home')">Sahara Saathi</span>
        </div>
        <nav class="hidden md:flex items-center gap-8">
            <a class="nav-link-top cursor-pointer text-orange-500 font-bold text-sm font-['Plus_Jakarta_Sans'] transition-all" onclick="switchTab('home')" data-target="home">Home</a>
            <a class="nav-link-top cursor-pointer text-slate-500 hover:text-blue-900 text-sm font-['Plus_Jakarta_Sans'] transition-all" onclick="switchTab('schemes')" data-target="schemes">Schemes</a>
            <a class="nav-link-top cursor-pointer text-slate-500 hover:text-blue-900 text-sm font-['Plus_Jakarta_Sans'] transition-all" onclick="switchTab('applications')" data-target="applications">Applications</a>
            <a class="nav-link-top cursor-pointer text-slate-500 hover:text-blue-900 text-sm font-['Plus_Jakarta_Sans'] transition-all" onclick="switchTab('profile')" data-target="profile">Profile</a>
        </nav>
        <div class="flex items-center gap-4">
            <button class="p-2 hover:bg-slate-100 rounded-full transition-colors hidden md:block" onclick="switchTab('schemes')">
                <span class="material-symbols-outlined text-on-surface-variant">search</span>
            </button>
            <button class="p-2 hover:bg-slate-100 rounded-full transition-colors relative" onclick="switchTab('applications')">
                <span class="material-symbols-outlined text-on-surface-variant">notifications</span>
                <span class="absolute top-2 right-2 w-2 h-2 bg-orange-500 rounded-full"></span>
            </button>
            <div class="w-10 h-10 rounded-full overflow-hidden border-2 border-surface-container-highest cursor-pointer" onclick="switchTab('profile')">
                <img alt="User Avatar" class="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDdyLbIIt_Y8J10gYHQ_tq_Upeo4xuAGg_roeL15PKrFg0s49sT2_ZlqEr1vciKI1JpK7ChTvKHgPxXOHObCqPkVTshvLrLJJzv1LiJpCVhJXTt13Z9uUjaQFj_UvwFikz7S0zQuRrKQ-iCbOBVITV8jURGxOF2oLMXO5Nf9Hi3wHDRwrPMO3Vb987JFGJR-d228y_97ptXdev6jashvk3rPhR1bGr6bSUnlJIlqGD3KuVWoR_l3tUywMb3GJnmErcaiTTGlMeilkfk"/>
            </div>
        </div>
    </header>

    <!-- Side Navigation (Mobile Hidden) -->
    <aside class="h-screen w-64 fixed left-0 top-0 bg-slate-50 border-r border-outline-variant/10 pt-24 pb-8 flex flex-col hidden md:flex z-40">
        <div class="px-6 flex flex-col gap-1 flex-1">
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
    <main class="md:pl-64 pt-24 min-h-screen">
        <div class="max-w-7xl mx-auto px-8 py-8 flex flex-col gap-12">

            <!-- ================= VIEW: HOME ================= -->
            <div id="view-home" class="view-section flex flex-col gap-12">
                <!-- Hero Search Section -->
                <section class="flex flex-col items-center text-center gap-8 py-12">
                    <div class="max-w-3xl flex flex-col gap-4">
                        <h1 class="text-5xl font-extrabold tracking-tighter text-primary font-headline">
                            Namaste, <span class="text-secondary-container">Rajesh</span>.
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
                                    <div class="bg-surface-container p-4 rounded-2xl rounded-tl-none text-sm text-on-surface leading-relaxed shadow-sm border border-slate-100">
                                        Hello Rajesh! I see your profile is verified. Click anywhere here to enlarge our chat room and ask me any queries!
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
                </div>
            </div>

            <!-- ================= VIEW: SCHEMES ================= -->
            <div id="view-schemes" class="view-section hidden-view flex flex-col gap-8">
                <div class="flex justify-between items-end">
                    <h2 class="text-4xl font-extrabold font-headline text-primary">All Schemes Explorer</h2>
                    <div class="flex gap-2">
                        <button class="px-4 py-2 border border-slate-200 rounded-lg text-sm font-bold flex items-center gap-2 hover:bg-slate-50"><span class="material-symbols-outlined text-base">filter_list</span> Filter</button>
                    </div>
                </div>
                <!-- Cloned instances for layout demo -->
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" id="schemes-grid-full">
                    <!-- We use JS to mirror the home cards into here on load for the demo! -->
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
                            <button class="w-12 h-12 rounded-full border border-slate-200 text-slate-400 hover:text-primary hover:bg-slate-50 flex items-center justify-center transition-all">
                                <span class="material-symbols-outlined">attach_file</span>
                            </button>
                            <input id="actualChatInput" class="chat-input-field flex-1 h-14 pl-6 pr-16 bg-white rounded-2xl border border-slate-200 outline-none focus:border-primary/50 focus:ring-4 focus:ring-primary/10 text-base shadow-sm font-label transition-all" placeholder="Describe your situation in Hindi, English, or Hinglish..." type="text" onkeypress="if(event.key === 'Enter') { triggerRAGAPI(this.value); this.value=''; }"/>
                            <button onclick="triggerRAGAPI(document.getElementById('actualChatInput').value); document.getElementById('actualChatInput').value='';" class="absolute right-3 top-3 bottom-3 w-10 bg-primary rounded-xl text-white flex items-center justify-center hover:bg-primary-container hover:scale-105 transition-all shadow-md">
                                <span class="material-symbols-outlined text-lg">send</span>
                            </button>
                        </div>
                        <div class="flex justify-center mt-4 text-xs text-slate-400 gap-6">
                            <span class="flex items-center gap-1"><span class="material-symbols-outlined text-[14px]">lock</span> Encrypted specific to your profile</span>
                            <span class="flex items-center gap-1 cursor-pointer hover:text-primary"><span class="material-symbols-outlined text-[14px]">mic</span> English / Hindi Voice input</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ================= VIEW: PROFILE ================= -->
            <div id="view-profile" class="view-section hidden-view flex flex-col gap-8">
                <h2 class="text-4xl font-extrabold font-headline text-primary">Citizen Profile</h2>
                <div class="grid md:grid-cols-3 gap-8">
                    <div class="col-span-1 bg-white p-8 rounded-[2rem] premium-shadow border border-slate-100 flex flex-col items-center text-center gap-4">
                        <div class="w-32 h-32 rounded-full overflow-hidden border-4 border-primary">
                            <img alt="User Avatar" class="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDdyLbIIt_Y8J10gYHQ_tq_Upeo4xuAGg_roeL15PKrFg0s49sT2_ZlqEr1vciKI1JpK7ChTvKHgPxXOHObCqPkVTshvLrLJJzv1LiJpCVhJXTt13Z9uUjaQFj_UvwFikz7S0zQuRrKQ-iCbOBVITV8jURGxOF2oLMXO5Nf9Hi3wHDRwrPMO3Vb987JFGJR-d228y_97ptXdev6jashvk3rPhR1bGr6bSUnlJIlqGD3KuVWoR_l3tUywMb3GJnmErcaiTTGlMeilkfk"/>
                        </div>
                        <div>
                            <h3 class="font-black text-2xl text-primary mt-2">Rajesh Kumar</h3>
                            <p class="text-on-surface-variant">ID: RJK-98213</p>
                        </div>
                        <div class="flex items-center gap-2 bg-green-100 text-green-700 px-4 py-2 rounded-full text-sm font-bold mt-2">
                            <span class="material-symbols-outlined text-base" style="font-variation-settings: 'FILL' 1;">verified</span> Verified Citizen
                        </div>
                    </div>
                    <div class="col-span-2 bg-white p-8 rounded-[2rem] premium-shadow border border-slate-100">
                        <h4 class="text-xl font-bold border-b pb-4 mb-6">Personal Details</h4>
                        <div class="grid grid-cols-2 gap-y-6 gap-x-12">
                            <div>
                                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">State</p>
                                <p class="font-bold text-primary">Rajasthan</p>
                            </div>
                            <div>
                                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Occupation</p>
                                <p class="font-bold text-primary">Agriculture</p>
                            </div>
                            <div>
                                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Category</p>
                                <p class="font-bold text-primary">OBC</p>
                            </div>
                            <div>
                                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Phone Number</p>
                                <p class="font-bold text-primary">+91 98xxx xxxx2</p>
                            </div>
                        </div>
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
    <div class="fixed bottom-8 left-1/2 -translate-x-1/2 md:translate-x-0 md:left-auto md:right-8 z-50 pointer-events-none">
        <div class="bg-secondary-fixed text-on-secondary-fixed px-6 py-3 rounded-full premium-shadow flex items-center gap-3 border border-secondary-container/20">
            <span class="material-symbols-outlined text-xl" style="font-variation-settings: 'FILL' 1;">verified_user</span>
            <span class="text-sm font-bold font-label">Your profile is 100% verified</span>
        </div>
    </div>

    <!-- JAVASCRIPT LOGIC -->
    <script>
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

            // Scroll to top
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // Initialize grid on load
        document.addEventListener("DOMContentLoaded", () => {
            // Clone scheme cards for the view-schemes grid
            const cards = document.querySelectorAll('#dashboard-scheme-cards .scheme-card-template');
            const targetGrid = document.getElementById('schemes-grid-full');
            if(cards.length > 0 && targetGrid) {
                cards.forEach(card => {
                    // clone twice just to pad out the grid for the demo
                    targetGrid.appendChild(card.cloneNode(true));
                    targetGrid.appendChild(card.cloneNode(true));
                    targetGrid.appendChild(card.cloneNode(true));
                });
            }

            // Standard welcome message for chat
            appendBotMessage("Hello Rajesh! I am Sahara AI. Please ask me any questions about government schemes or applications and I'll guide you step-by-step.");
        });

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
                    <span class="text-xs text-on-surface-variant font-medium">Sahara AI is thinking...</span>
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
                }

                const response = await fetch("/api/ask", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ query: queryText, session_id: window.chatSessionId })
                });
                
                const data = await response.json();
                removeLoading();
                
                if (data.answer) {
                    appendBotMessage(data.answer);
                } else {
                    appendBotMessage("Sorry, I encountered an error. Please try again.");
                }
            } catch (err) {
                console.error(err);
                removeLoading();
                appendBotMessage("Connection error. Ensure the server is running.");
            }
        }
    </script>
</body>
</html>
"""
