from pathlib import Path
import argparse, json, shutil, zipfile, os, re

OWNER = "RA Fahim"
BASE_URL = "https://rafahim.com/interview-prep"

questions = []
def add(category, slug, title, topic, difficulty, companies, languages, frequency, minutes, problem, approach, complexity, edges, related, front, back, custom=None):
    questions.append({"category":category,"slug":slug,"title":title,"topic":topic,"difficulty":difficulty,"companies":companies,"languages":languages,"frequency":frequency,"minutes":minutes,"problem":problem,"approach":approach,"complexity":complexity,"edges":edges,"related":related,"front":front,"back":back,"custom":custom or {}})

DSA = [
("two-sum","Two Sum","Arrays & Hashing","Easy",["Google","Amazon","Meta"],"একটি integer array এবং target দেওয়া আছে। এমন দুইটি আলাদা index ফেরত দাও যাদের মানের যোগফল target। প্রতিটি input-এ ঠিক একটি সমাধান আছে বলে ধরা যায়।","একটি hash map-এ আগে দেখা সংখ্যার index রাখো। বর্তমান x-এর জন্য target - x খুঁজে পেলে উত্তর পাওয়া যায়। প্রতিটি সংখ্যার জন্য পুরো array আবার খোঁজার দরকার হয় না।","O(n)","O(n)",["দুইটি সংখ্যার মান একই হতে পারে, কিন্তু index আলাদা হতে হবে।","একই element-কে দুইবার ব্যবহার করা যাবে না।","উত্তর array-র যেকোনো ক্রমে ফেরত দেওয়া যায়।"],["valid-anagram","contains-duplicate"],"Target-এর complement আগে দেখা গেছে কি না যাচাই করে এক pass-এ pair বের করার উপায় কী?","প্রতিটি x-এর জন্য target - x hash map-এ থাকলে pair পাওয়া যায়; না থাকলে x-এর index সংরক্ষণ করো।", "two_sum"),
("valid-parentheses","Valid Parentheses","Stack","Easy",["Amazon","Bloomberg","Microsoft"],"বন্ধনীযুক্ত string-এ (), [], {} সঠিকভাবে nested ও matched কি না নির্ধারণ করো।","Opening bracket stack-এ রাখো। Closing bracket এলে stack ফাঁকা কি না এবং top-এর bracket matching কি না পরীক্ষা করো। শেষে stack খালি হলে string valid।","O(n)","O(n)",["খালি string valid।","শুধু closing bracket থাকলে invalid।","ভিন্ন ধরনের bracket ভুলভাবে match হতে পারবে না।"],["implement-trie","reverse-linked-list"],"বন্ধনী যাচাইয়ে stack কেন উপযুক্ত?","সর্বশেষ খোলা bracket-ই আগে বন্ধ হওয়া প্রয়োজন—এটি LIFO নিয়ম; stack সেটিই স্বাভাবিকভাবে প্রকাশ করে।","valid_parentheses"),
("reverse-linked-list","Reverse Linked List","Linked List","Easy",["Amazon","Microsoft","Apple"],"একটি singly linked list-এর head দেওয়া আছে। pointer-এর দিক উল্টে reversed list-এর head ফেরত দাও।","prev, current ও next pointer ব্যবহার করো। প্রতিটি iteration-এ next সংরক্ষণ করে current.next-কে prev করো, তারপর pointer তিনটি এগিয়ে নাও।","O(n)","O(1)",["খালি list হলে null/None ফেরত দাও।","এক node-এর list-এ সেই node-ই head থাকবে।","নতুন node বানানোর প্রয়োজন নেই।"],["merge-two-sorted-lists","linked-list-cycle"],"In-place linked-list reversal-এ কোন তিনটি pointer কাজে লাগে?","prev আগের node, current বর্তমান node এবং next পরবর্তী node সংরক্ষণ করে; link উল্টানোর আগে next রেখে দিতে হয়।","reverse_linked_list"),
("merge-two-sorted-lists","Merge Two Sorted Lists","Linked List","Easy",["Amazon","Meta","Microsoft"],"দুইটি ascending sorted linked list দেওয়া আছে। একই sorted order-এ merge করে head ফেরত দাও।","একটি dummy node ও tail pointer নাও। দুই list-এর ছোট node-টি tail-এর সঙ্গে যুক্ত করে সংশ্লিষ্ট pointer এগিয়ে নাও; শেষে বাকি অংশ যুক্ত করো।","O(n + m)","O(1)",["একটি বা দুইটি list-ই খালি হতে পারে।","মূল node-গুলো reuse করা যায়।","দুই value সমান হলে যেকোনো list-এর node আগে আসতে পারে।"],["reverse-linked-list","linked-list-cycle"],"Dummy node ব্যবহারে কী সুবিধা?","প্রথম node আলাদা করে handle করতে হয় না। tail সর্বদা শেষ যুক্ত node নির্দেশ করে, তাই merge logic সরল হয়।","merge_two_sorted_lists"),
("maximum-subarray","Maximum Subarray","Dynamic Programming","Medium",["Amazon","Microsoft","LinkedIn"],"একটি non-empty integer array থেকে contiguous subarray-এর সর্বোচ্চ sum বের করো।","Kadane’s algorithm-এ বর্তমান অবস্থায় হয় নতুন subarray শুরু করি, নয়তো আগের running sum-এর সঙ্গে বর্তমান সংখ্যা যোগ করি। প্রতিটি ধাপে global best আপডেট হয়।","O(n)","O(1)",["সব সংখ্যা negative হলেও array non-empty হওয়ায় সবচেয়ে বড় element-ই উত্তর।","Subarray contiguous হতে হবে।","খালি subarray-এর sum শূন্য ধরে নেওয়া যাবে না।"],["climb-stairs","coin-change"],"Kadane’s algorithm-এ running sum কেন max(current, running + current) হয়?","আগের sum negative হলে সেটি যোগ করলে ফল খারাপ হবে; তখন নতুন subarray শুরু করা ভালো। নইলে আগের subarray চালিয়ে যাও।","maximum_subarray"),
("binary-search","Binary Search","Binary Search","Easy",["Google","Amazon","Microsoft"],"Ascending sorted array এবং target দেওয়া আছে। target-এর index বের করো; না থাকলে -1 ফেরত দাও।","low ও high দিয়ে search interval রাখো। মধ্যবর্তী value target-এর সমান হলে return; ছোট হলে low বাড়াও, বড় হলে high কমাও।","O(log n)","O(1)",["Array sorted হতে হবে।","Empty array হলে -1।","Mid হিসাবের overflow এড়াতে low + (high - low) // 2 প্যাটার্ন ব্যবহার করা যায়।"],["kth-largest-element","search-in-rotated-array"],"Binary search-এ sorted order কেন অপরিহার্য?","মধ্যবর্তী value দেখে কোন অর্ধেকে target থাকতে পারে তা বাদ দিতে order-এর তথ্য ব্যবহার করা হয়। unsorted array-তে এই সিদ্ধান্ত নির্ভরযোগ্য নয়।","binary_search"),
("best-time-to-buy-sell-stock","Best Time to Buy and Sell Stock","Arrays & Greedy","Easy",["Amazon","Meta","Bloomberg"],"প্রতিদিনের stock price-এর array দেওয়া আছে। একবার buy এবং পরে একবার sell করে সর্বোচ্চ profit বের করো; profit না হলে 0।","বাম থেকে ডানে minimum price এখন পর্যন্ত ধরে রাখো। প্রতিদিনের price থেকে minimum বাদ দিয়ে best profit আপডেট করো, তারপর minimum-ও update করো।","O(n)","O(1)",["এক দিনের data-তে transaction সম্ভব নয়, তাই 0।","দাম শুধু কমলে উত্তর 0।","Buy অবশ্যই sell-এর আগে।"],["maximum-subarray","two-sum"],"Stock profit সমস্যায় কেন আগের সর্বনিম্ন দাম রাখা যথেষ্ট?","প্রতিদিন sell করলে সম্ভাব্য সেরা buy হলো সেই দিনের আগে দেখা সর্বনিম্ন দাম। তাই সব buy-sell pair পরীক্ষা না করেও সেরা profit পাওয়া যায়।","best_time_stock"),
("contains-duplicate","Contains Duplicate","Arrays & Hashing","Easy",["Amazon","Apple","Google"],"Integer array-তে কোনো value একাধিকবার থাকলে true, নইলে false ফেরত দাও।","Set-এর মধ্যে value রাখো। কোনো value আগে থেকেই set-এ থাকলে duplicate পাওয়া গেছে; না থাকলে সেটি যোগ করো।","O(n) average","O(n)",["Empty array-তে duplicate নেই।","Negative integer-ও সাধারণ value।","Set operation average O(1), worst-case implementation-dependent।"],["two-sum","valid-anagram"],"Duplicate detection-এ sorting-এর বদলে set নিলে কী লাভ?","Set দিয়ে এক pass-এ average O(n) সময় পাওয়া যায়; sorting করলে সাধারণত O(n log n) এবং input order বদলে যেতে পারে।","contains_duplicate"),
("valid-anagram","Valid Anagram","Strings & Hashing","Easy",["Amazon","Google","Adobe"],"দুইটি string-এ একই character একই সংখ্যায় থাকলে true ফেরত দাও।","দুই string-এর length আগে তুলনা করো। তারপর character frequency count করো অথবা sorting করে তুলনা করো। এখানে frequency map ব্যবহার করা হবে।","O(n)","O(k)",["Case sensitivity স্পষ্ট করে নিতে হবে; এই version case-sensitive।","Unicode character থাকলে language-এর character iteration semantics বুঝতে হবে।","দৈর্ঘ্য আলাদা হলে সঙ্গে সঙ্গে false।"],["group-anagrams","two-sum"],"শুধু character set তুলনা করলে anagram সঠিকভাবে শনাক্ত হয় না কেন?","Set frequency উপেক্ষা করে। 'aab' এবং 'abb'-এর unique character একই হলেও count আলাদা; তাই frequency দরকার।","valid_anagram"),
("group-anagrams","Group Anagrams","Arrays & Hashing","Medium",["Amazon","Meta","Google"],"String-এর list-কে এমন group-এ ভাগ করো যেখানে প্রতিটি group-এর string-গুলো anagram।","প্রতিটি string-এর character frequency tuple-কে canonical key হিসেবে ব্যবহার করো। একই key-র string একই group-এ যাবে।","O(n · k log k)","O(n · k)",["Empty string-গুলোর key একই হবে।","Input-এ duplicate word থাকলে উভয় occurrence রাখতে হবে।","Unicode হলে fixed 26-counter key কেবল lowercase English-এর জন্য উপযুক্ত।"],["valid-anagram","top-k-frequent-elements"],"Group Anagrams-এ canonical key-এর কাজ কী?","Anagram-গুলোর character frequency একই থাকে, তাই frequency tuple একটি stable key; একই key পাওয়া string এক group-এ রাখা যায়।","group_anagrams"),
("longest-substring-without-repeating-characters","Longest Substring Without Repeating Characters","Sliding Window","Medium",["Amazon","Google","Bloomberg"],"একটি string-এর longest substring-এর length বের করো যেখানে কোনো character পুনরাবৃত্তি হয় না।","Sliding window-এর left pointer রাখো এবং প্রতিটি character-এর সর্বশেষ index map-এ সংরক্ষণ করো। duplicate current window-এর ভেতরে হলে left pointer তার পরের position-এ সরাও।","O(n)","O(k)",["Empty string-এর উত্তর 0।","একই character আগের window-এর বাইরে থাকলে left pointer পিছনে নেওয়া যাবে না।","Substring contiguous হতে হবে।"],["valid-anagram","group-anagrams"],"Sliding window-তে left pointer `max` দিয়ে update করার কারণ কী?","আগের duplicate index current window-এর বাইরে হতে পারে। left-কে পিছিয়ে দিলে ইতিমধ্যে বাতিল করা character আবার window-তে ঢুকে যাবে।","longest_substring"),
("product-of-array-except-self","Product of Array Except Self","Arrays & Prefix Sum","Medium",["Amazon","Microsoft","Apple"],"প্রতিটি index i-এর জন্য নিজের element বাদে বাকি সব element-এর product ফেরত দাও; division ব্যবহার করা যাবে না।","প্রথম pass-এ প্রতিটি অবস্থানে left-side product রাখো। দ্বিতীয় pass-এ ডানদিকের running product গুণ করে final result তৈরি করো।","O(n)","O(1) extra, output বাদে",["একটি zero থাকলে zero বাদে একটি অবস্থানে nonzero product থাকতে পারে।","দুই বা তার বেশি zero থাকলে সব ফল zero।","Division ব্যবহার নয়।"],["maximum-subarray","two-sum"],"Prefix ও suffix product একত্র করলে division লাগে না কেন?","প্রতিটি position-এর উত্তর হলো বাম পাশের product × ডান পাশের product। দুই pass-এ এই অংশগুলো জমা করলেই zero-র ক্ষেত্রও স্বাভাবিকভাবে কাজ করে।","product_except_self"),
("top-k-frequent-elements","Top K Frequent Elements","Hash Map & Heap","Medium",["Amazon","Google","Meta"],"Integer array এবং k দেওয়া আছে। frequency সবচেয়ে বেশি এমন kটি value ফেরত দাও।","Frequency map তৈরি করো। তারপর bucket sort-এ frequency অনুযায়ী value রাখো এবং highest frequency থেকে kটি value সংগ্রহ করো।","O(n)","O(n)",["সমাধান ধরে নেওয়া হয় k valid।","একই frequency-তে যেকোনো order গ্রহণযোগ্য যদি problem তা না নির্ধারণ করে।","Negative value-ও key হতে পারে।"],["group-anagrams","contains-duplicate"],"Bucket sort এই সমস্যায় কীভাবে O(n) average time দেয়?","কোনো frequency n-এর বেশি হতে পারে না। frequency-কে index ধরে bucket বানালে comparison-based sort ছাড়াই n থেকে 1 পর্যন্ত bucket scan করা যায়।","top_k_frequent"),
("number-of-islands","Number of Islands","Graphs & BFS/DFS","Medium",["Amazon","Google","Bloomberg"],"'1' ও '0' দিয়ে তৈরি grid-এ 4-directionally connected land cell-এর island সংখ্যা বের করো।","প্রতিটি unvisited land cell পেলে island count বাড়াও এবং DFS দিয়ে সম্পূর্ণ connected component mark করো। পরের scan-এ marked cell আর গণনা হবে না।","O(rows × cols)","O(rows × cols)",["Empty grid হলে 0।","Diagonal adjacency island যুক্ত করে না।","Recursive DFS খুব বড় grid-এ recursion limit ছাড়াতে পারে।"],["clone-graph","course-schedule"],"DFS-এ visited cell mark না করলে কী সমস্যা হয়?","একই land cell বারবার visit হতে পারে এবং প্রতিবেশীরা একে অন্যকে পুনরায় call করে অনন্ত recursion বা অতিরিক্ত কাজ তৈরি করতে পারে।","number_of_islands"),
("coin-change","Coin Change","Dynamic Programming","Medium",["Amazon","Google","Microsoft"],"Coin denomination array এবং amount দেওয়া আছে। amount তৈরি করতে minimum কয়টি coin লাগে? সম্ভব না হলে -1 ফেরত দাও; coin-এর supply অসীম।","dp[a] হলো amount a তৈরির minimum coin সংখ্যা। প্রতিটি coin c-এর জন্য a >= c হলে dp[a] = min(dp[a], dp[a-c] + 1)।","O(amount × number of coins)","O(amount)",["Amount 0 হলে উত্তর 0।","Positive coin denomination ধরে নেওয়া হয়েছে।","কোনো combination না থাকলে sentinel value থেকে -1 ফেরত দিতে হবে।"],["maximum-subarray","climb-stairs"],"Coin Change DP-তে amount ascending order-এ কেন iterate করা যায়?","Unlimited coin ব্যবহার করা যায়, তাই একই coin-এর আগের ছোট amount-এর state থেকে আবার ওই coin ব্যবহার করে বড় amount তৈরি করা অনুমোদিত।","coin_change"),
("climbing-stairs","Climbing Stairs","Dynamic Programming","Easy",["Amazon","Adobe","Google"],"প্রতিবার 1 বা 2 ধাপ নেওয়া গেলে n ধাপের সিঁড়িতে ওঠার মোট distinct উপায় গণনা করো।","শেষে পৌঁছানো যায় n-1 ধাপ থেকে 1 step অথবা n-2 ধাপ থেকে 2 steps নিয়ে। তাই recurrence Fibonacci: ways[n] = ways[n-1] + ways[n-2]।","O(n)","O(1)",["n অন্তত 1।","Base case ways[1]=1, ways[2]=2।","বড় n-এর জন্য language integer overflow খেয়াল রাখতে হবে।"],["coin-change","maximum-subarray"],"Climbing Stairs কেন Fibonacci recurrence?","শেষ move হয় 1 বা 2 step; তাই সব valid path-কে ways[n-1] ও ways[n-2] দুই disjoint group-এ ভাগ করা যায়।","climbing_stairs"),
("merge-intervals","Merge Intervals","Intervals & Sorting","Medium",["Google","Amazon","Bloomberg"],"[start, end] interval-এর list-কে overlapping interval merge করে ফেরত দাও।","Start অনুযায়ী sort করো। নতুন interval-এর start বর্তমান merged interval-এর end-এর মধ্যে পড়লে end বাড়াও; overlap না থাকলে নতুন interval শুরু করো।","O(n log n)","O(n)",["খালি list-এ খালি ফল।","একই endpoint-এ স্পর্শ করা interval overlap কি না problem statement দেখে নির্ধারণ করতে হবে; এখানে inclusive endpoint ধরা হয়েছে।","Input order sorted নাও হতে পারে।"],["binary-search","maximum-subarray"],"Interval merge-এর আগে sort কেন করা হয়?","Start অনুযায়ী সাজালে সম্ভাব্য overlap শুধু আগের merged interval-এর সঙ্গে পরীক্ষা করলেই হয়; অন্যথায় অনেক pair তুলনা করতে হতে পারে।","merge_intervals"),
("linked-list-cycle","Linked List Cycle","Linked List & Two Pointers","Easy",["Amazon","Microsoft","Google"],"Linked list-এর head দেওয়া আছে। কোনো node-এ আবার ফিরে আসা pointer cycle তৈরি করলে true ফেরত দাও।","Floyd’s tortoise-and-hare পদ্ধতিতে slow এক step, fast দুই step চলে। cycle থাকলে তারা মিলবে; fast null হলে cycle নেই।","O(n)","O(1)",["খালি list বা এক node-এর null next হলে cycle নেই।","Node value নয়, pointer identity তুলনা করতে হবে।","Fast pointer-এর next dereference করার আগে null check প্রয়োজন।"],["reverse-linked-list","merge-two-sorted-lists"],"Floyd algorithm cycle থাকলে কেন pointer-দুটি মিলবেই?","Cycle-এর মধ্যে fast pointer প্রতি iteration-এ slow-এর তুলনায় এক node করে দূরত্ব কমায়; finite cycle-এ এই modular distance একসময় শূন্য হয়।","linked_list_cycle"),
("kth-largest-element","Kth Largest Element in an Array","Heap & Selection","Medium",["Amazon","Google","Facebook"],"Unsorted integer array এবং k দেওয়া আছে। sorted order-এ k-th largest value ফেরত দাও।","k size-এর min-heap রাখো। প্রতিটি number heap-এ রাখার পর size k ছাড়ালে smallest pop করো; শেষে heap top হলো k-th largest।","O(n log k)","O(k)",["Duplicate value আলাদা array occurrence হিসেবে গণনা হয়।","k 1 থেকে array length-এর মধ্যে।","Negative number-এ min-heap logic অপরিবর্তিত।"],["top-k-frequent-elements","binary-search"],"k-th largest খুঁজতে size-k min-heap কেন কাজ করে?","Heap-এ সবসময় সবচেয়ে বড় kটি দেখা value রাখা হয়। তাদের মধ্যে smallest হলো পুরো দেখা অংশের k-th largest; সব element শেষে একই নিয়মের ফল চূড়ান্ত উত্তর।","kth_largest"),
("implement-trie","Implement Trie (Prefix Tree)","Trees & Strings","Medium",["Google","Microsoft","Amazon"],"Trie-তে insert(word), search(word), startsWith(prefix) implement করো।","প্রতি node-এ character অনুযায়ী child map এবং word শেষ হওয়ার boolean রাখো। প্রতিটি operation word-এর character ধরে path traverse করে।","O(L) per operation","O(total characters)",["Empty string insert/search semantics স্পষ্টভাবে সংজ্ঞায়িত করতে হবে; নিচের implementation empty word সমর্থন করে।","একই word বারবার insert করলে structure duplicate node তৈরি করে না।","Case-sensitive search।"],["valid-parentheses","group-anagrams"],"Trie-তে `isEnd` flag কেন দরকার?","কোনো prefix-এর path থাকা মানেই পুরো শব্দ insert হয়েছে নয়। `isEnd` ঠিক কোন node-এ inserted word শেষ হয়েছে তা ধরে রাখে।","implement_trie")]

for item in DSA:
    slug,title,topic,difficulty,companies,problem,approach,timec,spacec,edges,related,front,back,codekey = item
    add("dsa",slug,title,topic,difficulty,companies,["Python","JavaScript"],"High" if difficulty in ("Easy","Medium") else "Medium",20,problem,approach,{"time":timec,"space":spacec},edges,related,front,back,{"codekey":codekey})

SYSTEMS = [
("url-shortener","Design a URL Shortener","Distributed Systems","Medium",["Amazon","Google","Uber"],"দীর্ঘ URL থেকে ছোট code তৈরি, redirect, analytics এবং abuse prevention-সহ একটি URL-shortening service design করো.","শুরুতে API-কে create এবং redirect path-এ ভাগ করো। Create path URL validate করে unique short code বানিয়ে database-এ mapping লেখে; redirect path cache-এ code খুঁজে original URL-এ 301/302 দেয়।","Create: O(1) average lookup plus storage; redirect: cache hit-এ O(1) average","URLs, click events",["Code collision হলে retry করতে হবে।","Custom alias reserved word বা অন্য user-এর alias-এর সঙ্গে conflict করতে পারে।","Malicious URL, phishing, spam এবং hot keys-এর মোকাবিলা করতে হবে।"],["rate-limiter","search-autocomplete"],"Redirect traffic cache-এ রাখলে কী trade-off আসে?","Cache latency কমায় এবং database load কমায়, কিন্তু deletion/expiry-এর পর stale mapping কিছু সময় থাকতে পারে; TTL, invalidation এবং negative caching policy দরকার."),
("rate-limiter","Design a Rate Limiter","Distributed Systems","Medium",["Amazon","Stripe","Cloudflare"],"API-তে user/IP অনুযায়ী নির্দিষ্ট সময়ের মধ্যে request সীমিত করো, একাধিক application instance থাকলেও consistent থাকতে হবে.","Fixed window সহজ কিন্তু boundary burst তৈরি করে; sliding-window log accurate কিন্তু memory-heavy; token bucket burst allowance ও average rate-এর ভারসাম্য দেয়। Shared Redis atomic script দিয়ে distributed state update করা যায়.","O(1) per request for token bucket state","Per-identity counters/tokens",["Clock skew বা Redis outage-এর fallback policy দরকার।","Identity spoofing ঠেকাতে trusted proxy configuration প্রয়োজন।","Rate-limit response-এ Retry-After ও limit headers থাকা উপকারী।"],["url-shortener","notification-system"],"Token bucket-এ burst এবং steady rate কীভাবে নিয়ন্ত্রিত হয়?","Bucket-এ সময়ের সঙ্গে token জমে নির্দিষ্ট capacity পর্যন্ত; প্রতিটি request token খরচ করে। Bucket full থাকলে অল্প burst অনুমোদিত, কিন্তু token পুনরায় আসার গতি average rate সীমিত করে."),
("chat-system","Design a Real-Time Chat System","Real-Time Systems","Hard",["Meta","Slack","WhatsApp"],"One-to-one ও group chat, online presence, delivery status, offline message এবং history সমর্থন করে এমন chat system design করো.","WebSocket gateway persistent connections পরিচালনা করে। Message service authentication ও membership যাচাই করে durable store-এ message লেখে, তারপর broker-এর মাধ্যমে recipient connection-এ fan-out করে. Offline recipient-এর জন্য message sync cursor থাকে.","Send path broker/storage latency দ্বারা নির্ধারিত; history query indexed pagination","Messages, membership, delivery cursor, presence TTL",["একই message duplicate delivery হলে client message ID দিয়ে deduplicate করবে।","Group fan-out বড় হলে write-amplification বাড়ে; lazy fan-out বিবেচনা করা যায়।","Presence approximate হতে পারে; heartbeat timeout ও reconnect দরকার।"],["notification-system","news-feed"],"Chat message-এর durable write-এর আগে delivered দেখানো ঝুঁকিপূর্ণ কেন?","Storage commit-এর আগে acknowledgment দিলে server crash হলে user যে message পাঠানো হয়েছে ভাবছে সেটি হারাতে পারে। UI-তে sent এবং delivered আলাদা state রাখা উচিত."),
("news-feed","Design a News Feed","Feed & Ranking","Hard",["Meta","LinkedIn","Twitter"],"Follow graph, posts, ranking, pagination এবং high-follower creator-এর জন্য scalable news feed design করো.","Fan-out-on-write-এ creator post করলে follower feed-এ ID লিখে দ্রুত read পাওয়া যায়। Celebrities-এর ক্ষেত্রে fan-out-on-read বা hybrid model ব্যবহার করা যায়. Feed service candidate সংগ্রহ, ranking, filtering ও cursor pagination করে.","Read O(page size) after precompute; write cost depends on follower count","Posts, follows, feed entries, ranking signals",["Fan-out-on-write high-follower accounts-এ write spike তৈরি করে।","Pagination-এ stable cursor না থাকলে নতুন post-এ duplicate/skip হতে পারে।","Deleted/private post feed cache থেকেও filter করতে হবে।"],["chat-system","search-autocomplete"],"Hybrid feed fan-out কেন বাস্তবসম্মত?","সাধারণ creator-এর feed write-time-এ precompute করলে read দ্রুত হয়; বিশাল follower থাকা creator-এর সব follower-এ প্রতিবার write করা ব্যয়বহুল, তাই তাদের post read-time-এ merge করা যায়."),
("file-storage","Design a File Storage Service","Object Storage","Hard",["Google","Dropbox","Amazon"],"Upload/download, resumable large files, sharing links, version history এবং file metadata পরিচালনা করে এমন service design করো.","API service metadata ও permission পরিচালনা করে; bytes object storage-এ যায়। বড় upload-এর জন্য pre-signed multipart upload ব্যবহার করো; metadata database-এ checksum, owner, version এবং ACL রাখো. CDN download latency কমায়.","Metadata lookup O(1) indexed; transfer O(file size / bandwidth)","Object blobs, metadata, ACL, version manifest",["Upload complete হওয়ার আগে object published করা যাবে না।","Malware scanning এবং signed-link expiry দরকার।","Delete-এ metadata ও blob cleanup asynchronous হতে পারে।"],["url-shortener","ecommerce-checkout"],"Multipart upload-এর সুবিধা কী?","বড় file অংশে upload করে ব্যর্থ অংশ retry করা যায়; সব part যাচাই ও assemble হওয়ার পর object complete হয়, ফলে network interruption-এ শুরু থেকে upload করতে হয় না."),
("notification-system","Design a Notification System","Queues & Events","Medium",["Uber","Amazon","LinkedIn"],"Email, SMS, push ও in-app notification-কে preference, retry, deduplication এবং delivery tracking-সহ পাঠানোর system design করো.","Business event-কে outbox/queue-তে publish করো। Worker channel ও user preference দেখে provider call করে; attempts, response code এবং idempotency key সংরক্ষণ করে. Transient failure exponential backoff পায়; permanent failure dead-letter queue-তে যায়.","Enqueue O(1); delivery latency queue depth/provider SLA-এর ওপর নির্ভরশীল","Templates, user preferences, delivery attempts, provider IDs",["Provider timeout হলে send হয়েছিল কি না নিশ্চিত নাও হতে পারে; idempotency গুরুত্বপূর্ণ।","SMS/email consent এবং unsubscribe enforce করতে হবে।","Queue backlog monitor না করলে notification দেরি হবে।"],["rate-limiter","chat-system"],"Transactional outbox pattern কী সমস্যার সমাধান করে?","Database commit ও message publish আলাদা operation হলে একটির success আর অন্যটির failure হতে পারে। Outbox business data-র সঙ্গে একই transaction-এ event লেখে; publisher পরে retry করে."),
("ride-sharing","Design a Ride-Sharing Matching Service","Geospatial Systems","Hard",["Uber","Pathao","Grab"],"Rider request, nearby driver search, assignment, location updates, cancellation এবং surge conditions handle করো.","Driver app location periodic update করে। Geospatial index (geohash/H3/grid) nearby candidates shortlist করে; ETA ও vehicle constraints দিয়ে rank করে. Assignment-এর সময় atomic state transition/lease ব্যবহার করে এক driver-কে এক ride-এ match করো.","Nearby lookup roughly local-index query plus k candidates","Driver location, ride state, assignment lease, trip events",["GPS location stale হতে পারে; freshness threshold রাখো।","দুই dispatch worker একই driver assign করতে পারে; compare-and-set দরকার।","Sparse area-তে search radius ধাপে ধাপে বাড়াতে হয়।"],["rate-limiter","notification-system"],"একজন driver-কে concurrent request থেকে রক্ষা করবে কীভাবে?","Driver availability-তে atomic compare-and-set বা short lease ব্যবহার করো। Assignment সফল হওয়ার পর অন্য worker state transition করতে পারবে না; lease timeout হলে abandoned assignment release করা যায়."),
("video-streaming","Design a Video Streaming Platform","Media Delivery","Hard",["Netflix","YouTube","Amazon"],"Video upload, transcoding, adaptive bitrate playback, CDN delivery এবং view analytics architecture design করো.","Upload-এর পরে job queue transcoding pipeline চালায় এবং বিভিন্ন resolution/bitrate তৈরি করে। Manifest HLS/DASH segments নির্দেশ করে; CDN কাছের edge থেকে media serve করে. Metadata state machine upload, processing, ready ও failed অবস্থা track করে.","Playback startup depends on manifest and first segment; bandwidth scales with bitrate","Original media, segments, manifests, metadata, view events",["Transcoding retry idempotent হতে হবে।","CDN cache invalidation/versioned URLs দরকার।","Adaptive bitrate network variation দেখে quality বদলায়।"],["file-storage","notification-system"],"Adaptive bitrate কীভাবে buffering কমায়?","Player throughput ও buffer health estimate করে পরের segment-এর bitrate বেছে নেয়। Bandwidth কমলে lower-bitrate segment ব্যবহার করে playback চালিয়ে যেতে পারে."),
("ecommerce-checkout","Design an E-commerce Checkout","Payments & Transactions","Hard",["Amazon","Shopify","Stripe"],"Cart validation, stock reservation, payment authorization/capture, order creation, retry এবং refund নিয়ে reliable checkout design করো.","Checkout request idempotency key নিয়ে order attempt তৈরি করে। Inventory short reservation দেয়; payment provider authorization হয়; state machine order transition করে এবং durable events fulfillment-এ পাঠায়. Failure-এ reservation release ও reconciliation প্রয়োজন.","Critical path is bounded by inventory and payment provider latency","Orders, line items, inventory reservations, payment attempts, idempotency keys",["Client retry double charge করতে পারবে না।","Payment success কিন্তু callback হারালে reconciliation দরকার।","Stock reservation expiry এবং oversell control জরুরি।"],["notification-system","file-storage"],"Payment idempotency key কীভাবে double charge কমায়?","একই logical request retry হলে provider বা service একই key-র আগের ফল ফেরত দেয়; নতুন charge সৃষ্টি হয় না। Key-কে amount ও customer context-এর সঙ্গে bind করতে হবে."),
("search-autocomplete","Design Search Autocomplete","Search & Indexing","Medium",["Google","Amazon","LinkedIn"],"User typing-এর সঙ্গে low-latency suggestions, typo tolerance, popular queries এবং update support করো.","Prefix index বা trie candidate retrieve করে। Popular query count offline/stream process করে ranking score তৈরি করা যায়; top-k cache latency কমায়. Typo tolerance-এর জন্য n-gram/edit-distance stage সীমিত candidate-এর ওপর চালাও.","Prefix lookup O(prefix length + candidates) with trie/index","Query counts, prefix index, ranking features",["Very common prefixes huge candidate set তৈরি করতে পারে; top-k pruning দরকার।","Abusive/private query redact করা প্রয়োজন।","Index update eventual consistency হতে পারে।"],["news-feed","url-shortener"],"Autocomplete-এ prefix trie এবং inverted index-এর trade-off কী?","Trie prefix traversal-এ স্বাভাবিক, কিন্তু memory বেশি লাগতে পারে। Inverted index/search engine richer ranking ও typo tolerance দেয়, তবে query pipeline জটিল এবং resource-heavy হতে পারে.")]
for row in SYSTEMS:
    slug,title,topic,diff,companies,problem,approach,tc,sc,edges,related,front,back = row
    add("system-design",slug,title,topic,diff,companies,["Architecture","API Design"],"High",30,problem,approach,{"time":tc,"space":sc},edges,related,front,back)

DB = [
("database-indexes","Database Indexes: What, Why, and When?","Database Internals","Medium",["Amazon","Google","Daraz"],"Database index কীভাবে query দ্রুত করে, এবং index-এর cost কী?","সাধারণ B-tree index sorted key ও row reference রাখে, তাই equality/range filter-এ পুরো table scan এড়ানো যায়। কিন্তু insert/update/delete-এ index maintain করতে হয়; অতিরিক্ত index storage ও write latency বাড়ায়।","Index seek সাধারণত O(log n), তারপর matching row access","Index pages, table rows",["Low-selectivity column-এ index সবসময় লাভ দেয় না।","Composite index-এর column order গুরুত্বপূর্ণ।","Query planner-এর execution plan দেখে যাচাই করা দরকার।"],["acid-transactions","sql-joins"],"Write-heavy table-এ খুব বেশি index কেন ক্ষতিকর?","প্রতিটি write-এ সংশ্লিষ্ট index update হয়, ফলে disk I/O, storage ও transaction work বাড়ে। বাস্তব query plan-এ ব্যবহৃত index-ই রাখা ভালো."),
("acid-transactions","ACID Transactions","Database Internals","Medium",["Amazon","Stripe","Microsoft"],"ACID-এর চারটি property ব্যাখ্যা করো এবং money transfer-এ কেন দরকার বোঝাও।","Atomicity সব-or-nothing commit, consistency invariant বজায় রাখা, isolation concurrent transaction-এর interaction নিয়ন্ত্রণ, durability commit-এর পর crash থেকেও data স্থায়ী থাকা বোঝায়। Debit ও credit একই transaction-এ থাকলে partial transfer এড়ানো যায়।","Transaction complexity workload ও isolation level-এর ওপর নির্ভর করে","Transaction log, locks/MVCC versions",["Consistency rule schema constraints ও application invariant-এ enforce করতে হয়।","Isolation level অনুযায়ী anomaly আলাদা হয়।","Durability storage configuration-এর ওপরও নির্ভরশীল।"],["database-indexes","sql-joins"],"ACID-এর কোন property debit-কে credit ছাড়া commit হতে বাধা দেয়?","Atomicity দুই operation-কে একই logical transaction হিসেবে all-or-nothing করে। যেকোনো একটি operation ব্যর্থ হলে পুরো transaction rollback হওয়া উচিত."),
("sql-joins","SQL JOINs Explained","SQL","Easy",["Amazon","Daraz","Pathao"],"INNER, LEFT, RIGHT এবং FULL OUTER JOIN-এর পার্থক্য উদাহরণসহ ব্যাখ্যা করো।","INNER কেবল match; LEFT বাম table-এর সব row ও match থাকলে ডানদিকের data; RIGHT এর বিপরীত; FULL দুই পাশের unmatched row-ও রাখে। JOIN key-তে NULL ও duplicate থাকলে result cardinality বুঝতে হবে।","Output size depends on matched rows; proper indexes reduce lookup cost","Joined rows and execution plan",["One-to-many join row count বাড়ায়।","NULL equality comparison true হয় না; IS NULL ব্যবহার করো।","Duplicate key unexpected duplication তৈরি করতে পারে।"],["database-indexes","database-normalization"],"LEFT JOIN-এর right-side filter WHERE-এ দিলে LEFT JOIN কখন INNER JOIN-এর মতো আচরণ করতে পারে?","যদি WHERE clause right table-এর non-null field বাধ্যতামূলক করে, unmatched row-তে NULL হওয়ায় সেগুলো বাদ যায়। Outer-join filtering intent অনুযায়ী condition ON-এ রাখা লাগতে পারে."),
("database-normalization","Database Normalization","Database Design","Medium",["Microsoft","Amazon","Daraz"],"1NF, 2NF, 3NF কী এবং কী ধরনের anomalies কমায়?","1NF column-এ atomic value চায়; 2NF composite key-এর proper subset-এর ওপর partial dependency সরায়; 3NF non-key attribute-এর transitive dependency কমায়। Normalization update anomaly কমায়, কিন্তু সব read workload-এর জন্য অতিরিক্ত join ভালো নাও হতে পারে।","Design-time concept; query cost depends on joins","Normalized entities and foreign keys",["Primary key ও functional dependency চিনতে হবে।","Denormalization সচেতন performance trade-off।","Normalization মানে সব duplicate data স্বয়ংক্রিয়ভাবে নিষিদ্ধ নয়।"],["sql-joins","acid-transactions"],"Normalization update anomaly কমায় কীভাবে?","একই fact বহু row-তে copy থাকলে update-এর সময় কিছু row বদলে কিছু বাদ পড়তে পারে। Fact-কে এক authoritative place-এ রাখলে একই তথ্য একবার update করা যায়."),
("transactions-and-locking","Transactions, Locks, and MVCC","Database Concurrency","Hard",["Google","Stripe","Amazon"],"Concurrent transaction-এ dirty read, non-repeatable read, phantom এবং deadlock ব্যাখ্যা করো।","Locks conflicting access block করতে পারে; MVCC reader-কে snapshot version দেয়। Isolation level নির্ধারণ করে কোন anomaly সম্ভব। Deadlock হলে database সাধারণত transaction victim abort করে; application retry-কে bounded ও idempotent রাখতে হয়।","Depends on isolation level and contention","Locks, row versions, transaction log",["Long-running transaction vacuum/version cleanup আটকে দিতে পারে।","Deadlock-এর consistent lock order ঝুঁকি কমায়।","Retry করলে side effect duplicate হওয়ার সম্ভাবনা নিয়ন্ত্রণ করতে হবে।"],["acid-transactions","database-indexes"],"MVCC reader/writer contention কমাতে কীভাবে সাহায্য করে?","অনেক MVCC system reader-কে committed version-এর snapshot দেয়; ফলে reader সাধারণত writer-এর row lock-এর জন্য অপেক্ষা না করেই পড়ে। তবে old version cleanup এবং write-write conflict এখনও গুরুত্বপূর্ণ.")]
for row in DB:
    slug,title,topic,diff,companies,problem,approach,tc,sc,edges,related,front,back = row
    add("database",slug,title,topic,diff,companies,["SQL","PostgreSQL"],"High",20,problem,approach,{"time":tc,"space":sc},edges,related,front,back)

BEHAVIORAL = [
("tell-me-about-yourself","Tell Me About Yourself","Communication","Easy",["Local Startups","Product Companies","Remote Teams"],"এক মিনিটের মধ্যে relevant background, technical strength এবং role-এর সঙ্গে connection বোঝাও।","বর্তমান পরিচয় দিয়ে শুরু করো, প্রাসঙ্গিক project/skill-এর প্রমাণ দাও, তারপর এই role-এ কী contribution দিতে পারবে তা বলো। CV-এর প্রতিটি লাইন পড়ে শোনানোর দরকার নেই।","A concise answer usually takes 60–90 seconds","One clear story with one or two proof points",["Role-এর সঙ্গে সম্পর্কহীন personal details বাদ দাও।","নিজেকে একাধিক contradictory seniority label দিও না।","Claims-এর পেছনে concrete project example রাখো।"],["project-conflict","learning-new-skill"],"নিজের পরিচয় কীভাবে role-focused এবং সংক্ষিপ্ত রাখবে?","Present role/skill → relevant evidence → target role connection। কেবল সত্য project, tools এবং experience উল্লেখ করে উত্তরটি নিজের মতো করে মানিয়ে নাও.",{"star":{"situation":"আমি web development-এ কাজ ও শেখার মাধ্যমে frontend, backend এবং deployment-এর end-to-end flow বুঝতে শুরু করেছি।","task":"কেবল feature বানানো নয়, maintainable এবং user-friendly solution তৈরি করার দক্ষতা দেখাতে চেয়েছি।","action":"ছোট project-এ UI, API integration, data flow এবং responsive behavior হাতে-কলমে তৈরি করেছি; bug পেলে reproduce করে root cause খুঁজেছি।","result":"এতে requirements ভেঙে implement করা, trade-off বোঝা এবং কাজের ফল দেখিয়ে ব্যাখ্যা করার অভ্যাস তৈরি হয়েছে।"}}),
("project-conflict","Tell Me About a Technical Disagreement","Collaboration","Medium",["Google","Microsoft","Startups"],"কোনো teammate-এর সঙ্গে technical choice নিয়ে মতবিরোধ হলে কীভাবে সমাধান করেছ তা বোঝাও।","ব্যক্তিকে নয়, requirement ও evidence-কে কেন্দ্র করো। দুই option-এর reliability, cost, delivery time তুলনা করে ছোট experiment বা ADR-এ সিদ্ধান্ত নথিভুক্ত করা যায়।","Answer in 1–2 minutes","Decision rationale and outcome",["অন্যজনকে দোষারোপ করো না।","কৃতিত্ব নিজের নামে পুরোটা নিও না।","শিখন বা relationship outcome উল্লেখ করো।"],["tell-me-about-yourself","handling-feedback"],"Technical disagreement-এর উত্তর কীভাবে blame-free হবে?","সমস্যা নিরপেক্ষভাবে বলো, নিজের responsibility ও evidence ব্যাখ্যা করো, যৌথ সিদ্ধান্ত এবং ফলাফল জানাও; শেষে কী শিখেছ তা বলো.",{"star":{"situation":"একটি project-এ implementation-এর আগে feature দ্রুত ship করা এবং code reusable রাখা—এই দুই লক্ষ্য নিয়ে ভিন্ন মত ছিল।","task":"সময়ের মধ্যে deliver করতে হবে, আবার ভবিষ্যতের change-ও যেন অযথা কঠিন না হয় তা নিশ্চিত করা দরকার ছিল।","action":"আমি requirement-গুলো আলাদা করি, সবচেয়ে uncertain অংশের ছোট prototype প্রস্তাব করি এবং maintainability বনাম implementation time তুলনা করে team-এর feedback নিই।","result":"আলোচনা ব্যক্তিগত পছন্দ থেকে concrete trade-off-এ আসে, ছোট scope-এ সিদ্ধান্ত নেওয়া সহজ হয় এবং সিদ্ধান্তের কারণ লিখে রাখা যায়।"}}),
("production-bug","Describe a Bug You Investigated","Problem Solving","Medium",["Amazon","Google","Product Teams"],"Production বা project bug খুঁজে বের করার systematic approach STAR format-এ বোঝাও।","Impact establish করো, reproducible example তৈরি করো, logs/metrics inspect করো, smallest fix প্রয়োগ করো এবং regression test যোগ করো।","Answer in 1–2 minutes","Root cause and prevention",["Evidence ছাড়া root cause দাবি করো না।","Fix-এর validation step উল্লেখ করো।","Severity এবং user impact বোঝাও।"],["learning-new-skill","handling-feedback"],"Bug story-তে শুধু fix নয়, আর কী বলবে?","কীভাবে issue detect/reproduce করেছিলে, কোন hypothesis পরীক্ষা করেছিলে, কী test দিয়ে fix validate করেছিলে এবং পুনরাবৃত্তি রোধে কী করেছিলে—এসব বলো.",{"star":{"situation":"একটি web page-এ কিছু interaction expected মতো কাজ করছিল না এবং issue সব screen size-এ একভাবে দেখা যাচ্ছিল না।","task":"সমস্যাটি isolate করে existing behavior না ভেঙে fix করা প্রয়োজন ছিল।","action":"আমি reproduction steps লিখি, viewport ও browser condition আলাদা করে পরীক্ষা করি, console/network signals দেখি এবং smallest affected component-এ change করি।","result":"Fix-এর পর একই reproduction steps ও responsive checks আবার চালাই; ভবিষ্যৎ debugging-এর জন্য root cause ও verification note রেখে দিই।"}}),
("missed-deadline","Tell Me About a Missed Deadline","Ownership","Medium",["Amazon","Startups","Remote Teams"],"কাজ দেরি হলে ownership, communication এবং recovery plan কীভাবে দেখাবে?","কারণ ব্যাখ্যা করো কিন্তু excuse বানিও না। early communication, scope negotiation, task breakdown এবং future prevention দেখাও।","Answer in 1–2 minutes","Transparent recovery",["অন্য team member-কে দায়ী করো না।","Impact লুকিও না।","কী পরিবর্তন করেছ তা উল্লেখ করো।"],["project-conflict","handling-feedback"],"Deadline miss-এর গল্পে ownership কীভাবে বোঝাবে?","নিজের estimation বা communication gap স্বীকার করো, impact জানাও, recovery plan ও stakeholder update বর্ণনা করো এবং পরেরবার কী process বদলাবে বলো.",{"star":{"situation":"একটি project task-এ integration work-এর complexity প্রাথমিক estimate-এর চেয়ে বেশি বের হয়েছিল।","task":"Deadline risk দ্রুত জানিয়ে core requirement-এর delivery plan ঠিক করা দরকার ছিল।","action":"আমি dependency তালিকা করি, blocker ও remaining work স্পষ্ট করে share করি, optional polish আলাদা করি এবং ছোট milestones-এ progress update দিই।","result":"Team priority নিয়ে informed decision নিতে পারে; পরের estimate-এ integration/testing buffer ও earlier risk check অন্তর্ভুক্ত করি।"}}),
("learning-new-skill","Tell Me About a Skill You Learned Quickly","Growth Mindset","Easy",["Startups","Product Teams","Remote Teams"],"স্বল্প সময়ে নতুন tool/language শেখার উদাহরণ দাও এবং কীভাবে শেখা verify করেছিলে বোঝাও।","Learning goal নির্দিষ্ট করো, documentation ও ছোট project দিয়ে practice করো, unknown list track করো, feedback নিয়ে শেখা demonstrate করো।","Answer in 1–2 minutes","Evidence of applied learning",["শুধু course complete বলো না।","কী build করেছ তা বোঝাও।","Mistake থেকে শেখার উদাহরণ দাও।"],["tell-me-about-yourself","production-bug"],"Learning story-তে proof কী হতে পারে?","একটি working feature, test, small demo, code review feedback বা আগে না-পারা কাজ independently করতে পারা—এগুলো learning-এর evidence.",{"star":{"situation":"Project-এর একটি feature-এ নতুন library বা API ব্যবহার করার প্রয়োজন হয়েছিল।","task":"সময় সীমিত থাকলেও নিরাপদে working implementation তৈরি করতে হতো।","action":"আমি official documentation থেকে core concept শিখি, isolated example বানাই, failure case পরীক্ষা করি এবং পরে project-এ ছোট increment-এ integrate করি।","result":"Feature implement করার পাশাপাশি reusable notes তৈরি হয়, আর অনিশ্চিত behavior production path-এ নেওয়ার আগে test করা যায়।"}}),
("handling-feedback","Describe Feedback You Received","Communication","Easy",["Microsoft","Google","Product Teams"],"কোনো constructive feedback কীভাবে গ্রহণ করে কাজের উন্নতি করেছ তা বলো।","Feedback paraphrase করে বুঝে নাও, specific next action ঠিক করো এবং পরে পরিবর্তনের ফল যাচাই করো।","Answer in 1–2 minutes","Visible behavior change",["Feedback-কে attack হিসেবে উপস্থাপন করো না।","কেবল ‘আমি শিখেছি’ বলে শেষ করো না।","পরিবর্তনের evidence দাও।"],["project-conflict","missed-deadline"],"Feedback গ্রহণের প্রমাণ কীভাবে দেখাবে?","আগের আচরণ ও পরের আচরণ তুলনা করো—যেমন ছোট PR, earlier status update, tests আগে লেখা বা design decision document করা.",{"star":{"situation":"একটি review-এ feedback এসেছিল যে আমার implementation কাজ করলেও assumptions এবং testing rationale পরিষ্কারভাবে লেখা ছিল না।","task":"Reviewer এবং future maintainer-এর জন্য change বোঝা সহজ করা প্রয়োজন ছিল।","action":"আমি PR-এ context, alternatives এবং verification steps যুক্ত করি, complex logic ছোট করি এবং review-এর আগে test checklist চালাই।","result":"Review conversation বেশি focused হয় এবং একই ধরনের change-এর জন্য team-এর shared expectation পরিষ্কার হয়।"}}),
("teamwork-example","Describe a Successful Team Project","Teamwork","Medium",["Google","Amazon","Startups"],"কীভাবে collaboration করে shared result deliver করেছ তা explain করো।","Shared outcome, নিজের distinct contribution, coordination mechanism এবং result বলো। Team contribution ও নিজের কাজ আলাদা করো।","Answer in 1–2 minutes","Shared result and role clarity",["অন্যদের contribution মুছে ফেলো না।","সব কাজ নিজে করেছ এমন দাবি করো না।","Communication mechanism উল্লেখ করো।"],["project-conflict","tell-me-about-yourself"],"Teamwork উত্তর কীভাবে নিজের contribution পরিষ্কার রাখে?","Team-এর overall goal এক বাক্যে বলো; তারপর নিজের দায়িত্ব, coordination, blocked teammate-কে সাহায্য বা handoff এবং ফলাফল আলাদা করে বলো.",{"star":{"situation":"একটি shared project-এ UI, data integration এবং testing-এর কাজ একসঙ্গে এগোতে হতো।","task":"নিজের অংশ সম্পন্ন করার পাশাপাশি component handoff consistent রাখা দরকার ছিল।","action":"আমি expected data contract লিখে share করি, কাজ ছোট ভাগে ভাগ করি, integration point আগেই test করি এবং blocker হলে দ্রুত communicate করি।","result":"Parts একত্র করার সময় surprise কমে, issue early ধরা পড়ে এবং team একটি coherent deliverable তৈরি করতে পারে।"}}),
("handling-ambiguity","How Do You Handle Ambiguous Requirements?","Product Thinking","Medium",["Amazon","Startups","Product Teams"],"Requirement পুরোপুরি স্পষ্ট না হলে কীভাবে progress করবে এবং ভুল scope এড়াবে?","Unknown, assumption ও decision আলাদা করো। Stakeholder-এর কাছে outcome, constraints এবং acceptance criteria জানতে চাও; তারপর low-risk prototype বা milestone নিয়ে এগোও।","Answer in 1–2 minutes","Validated assumptions",["সব প্রশ্নের উত্তরের অপেক্ষায় নিষ্ক্রিয় থেকো না।","গুরুত্বপূর্ণ assumption নথিভুক্ত করো।","দ্রুত build করাই সবসময় সঠিক নয়।"],["missed-deadline","project-conflict"],"Ambiguous requirement-এ প্রথম কার্যকর পদক্ষেপ কী?","প্রথমে user outcome ও success criteria স্পষ্ট করো; তারপর reversible assumption ছোট experiment-এ validate করো এবং সিদ্ধান্ত record করো.",{"star":{"situation":"একটি feature request-এ desired outcome স্পষ্ট ছিল, কিন্তু edge case ও exact acceptance criteria পুরোপুরি নির্দিষ্ট ছিল না।","task":"সময় নষ্ট না করে ভুল assumption-এর ঝুঁকি কমানো দরকার ছিল।","action":"আমি প্রধান user flow ও unresolved questions লিখি, high-impact assumption stakeholder-এর সঙ্গে confirm করি এবং low-risk prototype দিয়ে interaction validate করি।","result":"Scope-এর গুরুত্বপূর্ণ অংশ আগেই পরিষ্কার হয় এবং implementation ও review-এর জন্য testable acceptance criteria পাওয়া যায়।"}}),
("failure-and-learning","Tell Me About a Failure","Resilience","Medium",["Google","Amazon","Product Teams"],"একটি ব্যর্থতা থেকে বাস্তব পরিবর্তন শেখার উদাহরণ দাও।","Failure-এর সীমা ও impact নির্দিষ্ট করো। নিজের সিদ্ধান্ত চিহ্নিত করো, recovery এবং prevention দেখাও।","Answer in 1–2 minutes","Concrete learning loop",["ছোট ভুলকে বড় নাটক বানিও না।","অন্য কাউকে scapegoat করো না।","বর্তমানে কী বদলেছে তা বলো।"],["missed-deadline","production-bug"],"Failure answer-কে credible করে কী?","ভুলটি বাস্তব ও সীমিত রাখো, নিজের অংশ স্পষ্ট করো এবং পরবর্তী project-এ প্রয়োগ করা specific process change উল্লেখ করো.",{"star":{"situation":"একবার কোনো task-এ final integration ও edge-case checking-এর effort প্রয়োজনের তুলনায় কম ধরে নেওয়া হয়েছিল।","task":"কাজটি usable অবস্থায় আনা এবং একই estimation mistake কমানো প্রয়োজন ছিল।","action":"আমি missing cases তালিকা করি, priority অনুযায়ী fix করি, review feedback নেই এবং পরবর্তী task breakdown-এ integration ও verification আলাদা item রাখি।","result":"কাজের estimate আরও realistic হয় এবং completion মানে শুধু happy path কাজ করা নয়—এই expectation পরিষ্কার হয়।"}}),
("why-should-we-hire-you","Why Should We Hire You?","Role Fit","Easy",["Local Startups","Product Companies","Remote Teams"],"Role-এর জন্য fit ব্যাখ্যা করো, অতিরঞ্জিত claim ছাড়া।","Job description-এর 2–3টি need-কে তোমার verified skill/project-এর সঙ্গে map করো, তারপর শেখার ক্ষেত্রের ব্যাপারেও honest থাকো।","Answer in 45–75 seconds","Evidence-to-role mapping",["Generic ‘hardworking’ কথায় আটকে থেকো না।","অজানা skill-এ expert দাবি করো না।","Company সম্পর্কে basic research করো।"],["tell-me-about-yourself","handling-ambiguity"],"এই উত্তরের গঠন কী?","Role-এর প্রয়োজন → relevant proof → team-এ সম্ভাব্য contribution → শেখার mental model. প্রতিটি claim-কে project বা example দিয়ে সমর্থন করো.",{"star":{"situation":"এই role-এ reliable feature delivery, clear communication এবং দ্রুত নতুন requirement বুঝে নেওয়া গুরুত্বপূর্ণ।","task":"আমার অভিজ্ঞতা কীভাবে role-এর প্রয়োজনের সঙ্গে মেলে তা দেখানো দরকার।","action":"আমি end-to-end project work, debugging approach এবং requirement-কে ছোট implementation step-এ ভাঙার অভ্যাসের উদাহরণ তুলে ধরি।","result":"Interview team আমার বর্তমান strength ও growth area দুটোই বুঝতে পারে; আমি যেখানে hands-on অভিজ্ঞতা কম সেখানে শেখার plan পরিষ্কারভাবে জানাই।"}})
]
for row in BEHAVIORAL:
    slug,title,topic,diff,companies,problem,approach,tc,sc,edges,related,front,back,custom = row
    add("behavioral",slug,title,topic,diff,companies,["Communication","STAR"],"Medium",10,problem,approach,{"time":tc,"space":sc},edges,related,front,back,custom)

LANGUAGES = [
("python-list-vs-tuple","Python List vs Tuple","Python","Easy",["Amazon","Local Startups"],"Python list এবং tuple-এর মধ্যে পার্থক্য, ব্যবহার এবং mutability-এর প্রভাব ব্যাখ্যা করো।","List mutable, তাই append বা item assignment করা যায়। Tuple immutable sequence; fixed record বা hashable collection key হিসেবে কাজে লাগতে পারে যদি সব element hashable হয়। Tuple-এর immutability shallow—এর ভেতরে mutable object থাকলে সেটি বদলাতে পারে।","List/tuple access O(1) by index","References to contained objects",["Tuple nested mutable object-কে immutable বানায় না।","List সাধারণত dictionary key হতে পারে না।","Performance difference সাধারণত semantics-এর চেয়ে কম গুরুত্বপূর্ণ।"],["python-gil","memory-garbage-collection"],"Tuple সবসময় immutable data structure বোঝায় কি?","Tuple-এর element binding বদলানো যায় না, কিন্তু tuple-এর মধ্যে থাকা list-এর content বদলাতে পারে। তাই immutability top-level sequence-এ প্রযোজ্য।"),
("javascript-event-loop","Explain the JavaScript Event Loop","JavaScript Runtime","Medium",["Google","Amazon","Frontend Teams"],"Call stack, task queue, microtask queue এবং event loop-এর সম্পর্ক ব্যাখ্যা করো।","Synchronous stack আগে চলে। Stack empty হলে microtasks যেমন Promise callbacks সাধারণত পরবর্তী task-এর আগে drain হয়; timers ও I/O callback task scheduling-এর মাধ্যমে পরে চলে। Exact host details browser ও Node.js-এ কিছুটা আলাদা।","Depends on each callback; one long callback blocks the thread","Task and microtask queues",["setTimeout(..., 0) immediate execution বোঝায় না।","Microtask loop অনবরত চললে rendering starve করতে পারে।","Node event loop phases browser-এর সঙ্গে এক নয়।"],["javascript-closures","javascript-async"],"Resolved Promise callback setTimeout callback-এর আগে কেন চলতে পারে?","Promise reaction microtask queue-তে schedule হয়; current synchronous stack-এর পরে microtasks process হয়, আর timer callback future task হিসেবে execute হয়।"),
("javascript-closures","JavaScript Closures","JavaScript","Medium",["Google","Meta","Frontend Teams"],"Closure কী এবং loop, callback বা private state-এ এটি কীভাবে কাজে লাগে বোঝাও।","Inner function lexical environment থেকে বাইরের variable access করতে পারে, outer function return হওয়ার পরেও। এটি callback ও factory-তে useful, কিন্তু বড় captured object ধরে রাখলে memory lifetime দীর্ঘ হতে পারে।","Function call cost plus captured-variable access","Captured lexical environment",["Closure value-এর snapshot নয়; variable binding access করে।","var loop capture-এর classic problem let দিয়ে সমাধান করা যায়।","Unintended retention memory leak-এর মতো symptom দিতে পারে।"],["javascript-event-loop","javascript-async"],"Closure-এ variable-এর snapshot থাকে নাকি binding?","সাধারণ closure lexical binding-এর reference ব্যবহার করে; function call-এর সময় সেই binding-এর বর্তমান value পড়তে পারে।"),
("typescript-type-vs-interface","TypeScript type vs Interface","TypeScript","Easy",["Microsoft","Frontend Teams","Startups"],"Type alias এবং interface কীভাবে object shape, union, extension ও declaration merging handle করে?","Interface object contract ও declaration merging-এর জন্য সুবিধাজনক; type alias union, intersection, primitive alias ও mapped type-এ flexible. অধিকাংশ object-shape use case-এ দুটোই উপযুক্ত; team convention consistency বেশি গুরুত্বপূর্ণ।","Compile-time only; no runtime performance impact","Type checker metadata",["type alias runtime validator তৈরি করে না।","Interface সব advanced type expression প্রকাশ করতে পারে না।","Public library API-তে declaration merging intentional কি না বিবেচনা করো।"],["javascript-event-loop","javascript-async"],"TypeScript type annotation কি runtime input validate করে?","না। TypeScript compile-time type checking করে এবং type information সাধারণত emit-এর সময় মুছে যায়। External input-এর জন্য runtime schema validation প্রয়োজন।"),
("python-gil","What Is Python's GIL?","Python Runtime","Medium",["Backend Teams","Startups"],"CPython-এর Global Interpreter Lock-এর কাজ এবং threading বনাম multiprocessing trade-off explain করো।","Traditional CPython build-এ GIL এক সময়ে একটি thread-কে Python bytecode execute করতে দেয়, ফলে CPU-bound pure Python thread সাধারণত একাধিক core-এ parallel speedup পায় না। I/O-bound threads অপেক্ষার সময়ে progress করতে পারে; multiprocessing আলাদা process ব্যবহার করে।","Depends on workload and process/thread model","Thread stacks or process memory",["সব Python implementation ও build-এ একই GIL behavior ধরে নেওয়া যাবে না।","Multiprocessing IPC ও memory overhead আনে।","Native extensions GIL release করতে পারে।"],["python-list-vs-tuple","memory-garbage-collection"],"I/O-bound workload-এ threading কেন তবু ভালো হতে পারে?","Network বা disk wait-এর সময় একটি thread block হলেও অন্য thread কাজ করতে পারে; তাই GIL থাকা সত্ত্বেও latency hide ও concurrency উন্নত হতে পারে।"),
("javascript-async","Promises and async/await","JavaScript Async","Medium",["Amazon","Google","Frontend Teams"],"Promise chain ও async/await দিয়ে asynchronous error handling এবং parallel task management বোঝাও।","async function সবসময় Promise ফেরত দেয়। await rejection হলে try/catch-এ ধরা যায়। Independent operation sequential await না করে Promise.all-এ চালালে wall-clock latency কমতে পারে, কিন্তু Promise.all fail-fast এবং cancellation নিজে থেকে করে না।","Runtime depends on operations; independent work can overlap","Promise objects and task state",["await সব operation parallel করে না।","Promise.all partial results return করে না যখন reject হয়।","Unhandled rejection logging ও cleanup দরকার।"],["javascript-event-loop","javascript-closures"],"দুইটি independent request-এর আগে আগে await দিলে latency বাড়তে পারে কেন?","Sequential awaits প্রথমটি শেষ না হওয়া পর্যন্ত দ্বিতীয়টি start করে না। দুইটি Promise আগে তৈরি করে Promise.all দিলে অপেক্ষা overlap করতে পারে।"),
("memory-garbage-collection","Memory Management and Garbage Collection","Runtime Internals","Medium",["Google","Microsoft","Backend Teams"],"Garbage collector reachability ব্যবহার করে memory মুক্ত করে কীভাবে এবং memory leak কেন হয়?","Tracing GC-তে roots থেকে reachable object mark করা হয়, unreachable object collect করা যায়। Garbage-collected language-এও event listener, timer, global cache বা closure-এর reference object reachable রাখলে memory leak হতে পারে।","GC pause and cost depend on runtime/heap","Heap objects, roots, references",["GC থাকা মানে memory leak অসম্ভব নয়।","Finalizer timing deterministic নাও হতে পারে।","Heap growth দেখে একা leak প্রমাণ হয় না; allocation/retention profile করো।"],["python-gil","python-list-vs-tuple"],"Garbage-collected app-এও memory leak কীভাবে সম্ভব?","Object আর ব্যবহার না করলেও reachable reference থাকলে collector সেটি মুছতে পারে না; long-lived map বা detached DOM reference তার উদাহরণ।"),
("javascript-this","How Does `this` Work in JavaScript?","JavaScript","Medium",["Google","Meta","Frontend Teams"],"Regular function এবং arrow function-এ `this` কীভাবে নির্ধারিত হয়?","Regular function call-site অনুযায়ী this পায়—method call, explicit bind/call/apply, constructor বা strict-mode standalone call। Arrow function নিজস্ব this bind করে না; lexical surrounding scope থেকে নেয়।","No special algorithmic complexity","Execution context binding",["Function কোথায় লেখা হয়েছে তা সবসময় regular function-এর this নির্ধারণ করে না।","Arrow function method হিসেবে সাধারণত উপযুক্ত নয় যদি dynamic this দরকার হয়।","Class method callback-এ binding খেয়াল করতে হবে।"],["javascript-closures","javascript-event-loop"],"Arrow function-এর `this` কেন surrounding object-এর dynamic receiver নয়?","Arrow function নিজস্ব this binding তৈরি করে না; definition-এর lexical environment থেকে this নেয়। তাই call-site বদলালেও সেটি rebind হয় না।"),
("api-error-handling","Reliable API Error Handling","Backend Engineering","Medium",["Amazon","Stripe","Startups"],"API error response কীভাবে consistent, debuggable এবং safe রাখা যায়?","Stable machine-readable error code, human message, request ID এবং appropriate HTTP status দাও। Internal stack trace বা secret client-কে দিও না। Validation, authentication, conflict, rate limit ও transient server failure আলাদা করো; retry policy idempotency বুঝে নির্ধারণ করো।","O(1) error mapping plus logging overhead","Structured logs and request context",["500 status-এ sensitive trace ফেরত দিও না।","Client validation error retry করা উচিত নয় সাধারণত।","Retry storm এড়াতে backoff ও jitter দরকার।"],["javascript-async","transactions-and-locking"],"Retryable error আর non-retryable error আলাদা করা জরুরি কেন?","Validation বা authorization error retry করলে সমাধান হয় না; transient timeout retry করলে সফল হতে পারে। Status/code ও idempotency দেখে bounded retry policy করা উচিত।"),
("http-caching","HTTP Caching: Cache-Control, ETag, and CDN","Web Protocols","Medium",["Google","Amazon","Frontend Teams"],"Browser/CDN cache কীভাবে latency কমায় এবং stale content নিয়ন্ত্রণ করে?","Cache-Control freshness ও shared/private caching নির্দেশ করে; ETag conditional request-এ resource unchanged হলে 304 দেয়। Hashed static assets long immutable cache পেতে পারে, কিন্তু personalized response public cache-এ দেওয়া বিপজ্জনক।","Cache hit reduces origin work; miss depends on origin","Cache entries and validators",["Authorization/personal data cache policy সতর্কভাবে করতে হবে।","ETag validation freshness policy-এর বিকল্প নয়।","Versioned asset URL invalidation সহজ করে।"],["url-shortener","file-storage"],"ETag আর max-age-এর পার্থক্য কী?","max-age বলে response কতক্ষণ fresh ধরা যাবে। ETag একটি validator; stale entry revalidate করতে server-কে জিজ্ঞাসা করলে content একই হলে 304 ফেরত দিতে পারে।")]
for row in LANGUAGES:
    slug,title,topic,diff,companies,problem,approach,tc,sc,edges,related,front,back = row
    add("languages",slug,title,topic,diff,companies,["Python","JavaScript","TypeScript"],"Medium",15,problem,approach,{"time":tc,"space":sc},edges,related,front,back)

BD = [
("bd-self-introduction","Tell Me About Yourself for a Bangladesh Tech Role","Interview Communication","Easy",["Bangladesh Startups","Software Firms","Remote Teams"],"বাংলাদেশের software company-তে junior web developer interview-তে 60–90 সেকেন্ডের পরিচয় কীভাবে দেবে?","বাংলা বা ইংরেজি—যে ভাষায় interview চলছে সেই ভাষায় structured introduction দাও: current focus, relevant skills, one concrete project, target role-এ আগ্রহ। CV-এর বাইরে অপ্রাসঙ্গিক ব্যক্তিগত তথ্য বাদ রাখো।","60–90 seconds","One short story and a project proof",["যে experience নেই তা দাবি কোরো না।","Company-এর কাজ না জেনে generic praise দিও না।","বাংলা-ইংরেজি technical vocabulary স্বাভাবিকভাবে ব্যবহার করতে পারো।"],["tell-me-about-yourself","why-should-we-hire-you"],"বাংলাদেশি tech interview-তে introduction-এর core structure কী?","বর্তমান focus → relevant skill → demonstrable project → role fit. নির্দিষ্ট project-এ নিজের actual contribution ও শেখা বিষয় উল্লেখ করো."),
("bd-salary-expectation","How to Discuss Salary Expectations in Bangladesh","Career Planning","Medium",["Bangladesh Startups","Software Firms","Remote Teams"],"বাংলাদেশে salary expectation প্রশ্নে কীভাবে research-based এবং flexible answer দেবে?","Role level, location, total compensation, probation policy এবং benefits অনুযায়ী market range research করো। নিজের target range বলার আগে role scope ও budget জিজ্ঞেস করা যায়; gross/net, bonus এবং review cycle স্পষ্ট করো।","A concise range with rationale","Compensation criteria",["একটি যাচাইহীন market number-কে universal benchmark বলো না।","Gross salary, take-home এবং benefits আলাদা।","নিজের minimum না ভেবে খুব কম offer accept করে ফেলো না।"],["bd-notice-period","why-should-we-hire-you"],"Salary expectation-এ কী কী clarify করবে?","Monthly gross না net, probation salary, festival bonus, performance review, insurance/benefit, remote allowance এবং role-এর responsibilities clarify করো; range-এর flexibility ও rationale জানাও."),
("bd-notice-period","Notice Period and Joining Date","Workplace Basics","Easy",["Bangladesh Startups","Software Firms","Remote Teams"],"Notice period, current commitment এবং joining availability professional ভাবে কীভাবে জানাবে?","Employment agreement বা current policy দেখে accurate joining date বলো। Handover responsibly plan করো; offer নিশ্চিত হওয়ার আগে current role ছেড়ে দেওয়ার প্রতিশ্রুতি দিও না।","30–45 seconds","A realistic date plus handover plan",["চুক্তি না দেখে notice period অনুমান কোরো না।","Current employer সম্পর্কে negative মন্তব্য কোরো না।","Availability বদলালে early update দাও।"],["missed-deadline","bd-salary-expectation"],"Joining date বলার আগে কী verify করবে?","চুক্তি/প্রযোজ্য policy-তে notice requirement, pending handover এবং actual last working date নিশ্চিত করো; তারপর realistic joining date জানাও."),
("bd-remote-work","Working with Remote or International Teams from Bangladesh","Remote Work","Medium",["Remote Teams","Product Companies","Freelance Teams"],"বাংলাদেশ থেকে international team-এর সঙ্গে remote collaboration-এর readiness কীভাবে দেখাবে?","Async writing, clear status, timezone overlap, reliable connectivity, security, estimates ও blockers আগে জানানো—এসব concrete workflow দিয়ে বোঝাও।","Answer in 1–2 minutes","Reliable async delivery",["শুধু ‘internet আছে’ বলা যথেষ্ট নয়।","Timezone commitment বাস্তবসম্মত রাখো।","Client/customer data personal device-এ নিরাপদে রাখো।"],["teamwork-example","handling-ambiguity"],"Remote readiness-এর সবচেয়ে শক্ত evidence কী?","Written update, documented handoff, predictable availability, task tracking, secure access এবং blocker early escalate করার concrete example."),
("bd-junior-experience-gap","Answering Limited Experience as a Junior Developer","Career Growth","Easy",["Bangladesh Startups","Software Firms","Remote Teams"],"Professional experience কম হলে কীভাবে honest থেকে readiness দেখাবে?","Experience gap লুকিও না। Relevant portfolio project, fundamentals, code quality, debugging method এবং feedback থেকে শেখার উদাহরণ দেখাও। চাকরির বাস্তব production exposure কম হলে সেটি সরাসরি বলো।","45–75 seconds","Evidence of fundamentals and learning",["Personal project-কে production employment বলে উপস্থাপন করো না।","Technologies তালিকা না দিয়ে depth দেখাও।","একটি known gap-এর learning plan জানাও।"],["learning-new-skill","tell-me-about-yourself"],"Junior হিসেবে credibility কীভাবে তৈরি করবে?","নিজের হাতে build করা feature, design decision, test/debugging example দেখাও। কোন অংশে সাহায্য নিয়েছ এবং এখন কীভাবে বুঝতে পারো তা স্বচ্ছভাবে ব্যাখ্যা করো.")]
for row in BD:
    slug,title,topic,diff,companies,problem,approach,tc,sc,edges,related,front,back = row
    add("bangladesh",slug,title,topic,diff,companies,["Interview","Career"],"Medium",10,problem,approach,{"time":tc,"space":sc},edges,related,front,back)

if len(questions) != 60:
    raise RuntimeError(f"Expected 60 questions, found {len(questions)}")

PY_SOLUTIONS = {
"two_sum": '''def two_sum(nums, target):
    seen = {}
    for i, value in enumerate(nums):
        need = target - value
        if need in seen:
            return [seen[need], i]
        seen[value] = i
    return []''',
"valid_parentheses": '''def is_valid(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []
    for char in s:
        if char in '([{':
            stack.append(char)
        elif not stack or stack.pop() != pairs.get(char):
            return False
    return not stack''',
"reverse_linked_list": '''def reverse_list(head):
    prev = None
    current = head
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    return prev''',
"merge_two_sorted_lists": '''def merge_two_lists(list1, list2):
    dummy = ListNode(0)
    tail = dummy
    while list1 and list2:
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next
    tail.next = list1 if list1 else list2
    return dummy.next''',
"maximum_subarray": '''def max_subarray(nums):
    best = current = nums[0]
    for value in nums[1:]:
        current = max(value, current + value)
        best = max(best, current)
    return best''',
"binary_search": '''def binary_search(nums, target):
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = low + (high - low) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1''',
"best_time_stock": '''def max_profit(prices):
    minimum = float('inf')
    best = 0
    for price in prices:
        minimum = min(minimum, price)
        best = max(best, price - minimum)
    return best''',
"contains_duplicate": '''def contains_duplicate(nums):
    seen = set()
    for value in nums:
        if value in seen:
            return True
        seen.add(value)
    return False''',
"valid_anagram": '''from collections import Counter

def is_anagram(s, t):
    return Counter(s) == Counter(t)''',
"group_anagrams": '''from collections import defaultdict, Counter

def group_anagrams(strs):
    groups = defaultdict(list)
    for word in strs:
        key = tuple(sorted(Counter(word).items()))
        groups[key].append(word)
    return list(groups.values())''',
"longest_substring": '''def length_of_longest_substring(s):
    last_seen = {}
    left = 0
    best = 0
    for right, char in enumerate(s):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1
        last_seen[char] = right
        best = max(best, right - left + 1)
    return best''',
"product_except_self": '''def product_except_self(nums):
    result = [1] * len(nums)
    prefix = 1
    for i, value in enumerate(nums):
        result[i] = prefix
        prefix *= value
    suffix = 1
    for i in range(len(nums) - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]
    return result''',
"top_k_frequent": '''def top_k_frequent(nums, k):
    from collections import Counter
    counts = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for value, count in counts.items():
        buckets[count].append(value)
    result = []
    for count in range(len(buckets) - 1, 0, -1):
        for value in buckets[count]:
            result.append(value)
            if len(result) == k:
                return result
    return result''',
"number_of_islands": '''def num_islands(grid):
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                stack = [(r, c)]
                grid[r][c] = '0'
                while stack:
                    x, y = stack.pop()
                    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == '1':
                            grid[nx][ny] = '0'
                            stack.append((nx, ny))
    return count''',
"coin_change": '''def coin_change(coins, amount):
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    for value in range(1, amount + 1):
        for coin in coins:
            if coin <= value:
                dp[value] = min(dp[value], dp[value - coin] + 1)
    return dp[amount] if dp[amount] <= amount else -1''',
"climbing_stairs": '''def climb_stairs(n):
    if n <= 2:
        return n
    one, two = 1, 2
    for _ in range(3, n + 1):
        one, two = two, one + two
    return two''',
"merge_intervals": '''def merge_intervals(intervals):
    if not intervals:
        return []
    intervals = sorted(intervals, key=lambda item: item[0])
    merged = [intervals[0][:]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged''',
"linked_list_cycle": '''def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False''',
"kth_largest": '''import heapq

def find_kth_largest(nums, k):
    heap = []
    for value in nums:
        heapq.heappush(heap, value)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]''',
"implement_trie": '''class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.is_end

    def starts_with(self, prefix):
        return self._walk(prefix) is not None

    def _walk(self, text):
        node = self.root
        for char in text:
            if char not in node.children:
                return None
            node = node.children[char]
        return node'''
}

JS_SOLUTIONS = {
"two_sum": '''function twoSum(nums, target) {
  const seen = new Map();
  for (let i = 0; i < nums.length; i += 1) {
    const need = target - nums[i];
    if (seen.has(need)) return [seen.get(need), i];
    seen.set(nums[i], i);
  }
  return [];
}''',
"valid_parentheses": '''function isValid(s) {
  const pairs = { ")": "(", "]": "[", "}": "{" };
  const stack = [];
  for (const char of s) {
    if (char === "(" || char === "[" || char === "{") stack.push(char);
    else if (stack.length === 0 || stack.pop() !== pairs[char]) return false;
  }
  return stack.length === 0;
}''',
"reverse_linked_list": '''function reverseList(head) {
  let previous = null;
  let current = head;
  while (current !== null) {
    const nextNode = current.next;
    current.next = previous;
    previous = current;
    current = nextNode;
  }
  return previous;
}''',
"merge_two_sorted_lists": '''function mergeTwoLists(list1, list2) {
  const dummy = new ListNode(0);
  let tail = dummy;
  while (list1 !== null && list2 !== null) {
    if (list1.val <= list2.val) {
      tail.next = list1;
      list1 = list1.next;
    } else {
      tail.next = list2;
      list2 = list2.next;
    }
    tail = tail.next;
  }
  tail.next = list1 !== null ? list1 : list2;
  return dummy.next;
}''',
"maximum_subarray": '''function maxSubArray(nums) {
  let current = nums[0];
  let best = nums[0];
  for (let i = 1; i < nums.length; i += 1) {
    current = Math.max(nums[i], current + nums[i]);
    best = Math.max(best, current);
  }
  return best;
}''',
"binary_search": '''function binarySearch(nums, target) {
  let low = 0;
  let high = nums.length - 1;
  while (low <= high) {
    const mid = low + Math.floor((high - low) / 2);
    if (nums[mid] === target) return mid;
    if (nums[mid] < target) low = mid + 1;
    else high = mid - 1;
  }
  return -1;
}''',
"best_time_stock": '''function maxProfit(prices) {
  let minimum = Infinity;
  let best = 0;
  for (const price of prices) {
    minimum = Math.min(minimum, price);
    best = Math.max(best, price - minimum);
  }
  return best;
}''',
"contains_duplicate": '''function containsDuplicate(nums) {
  const seen = new Set();
  for (const value of nums) {
    if (seen.has(value)) return true;
    seen.add(value);
  }
  return false;
}''',
"valid_anagram": '''function isAnagram(s, t) {
  if (s.length !== t.length) return false;
  const counts = new Map();
  for (const char of s) counts.set(char, (counts.get(char) || 0) + 1);
  for (const char of t) {
    const count = counts.get(char);
    if (!count) return false;
    if (count === 1) counts.delete(char);
    else counts.set(char, count - 1);
  }
  return counts.size === 0;
}''',
"group_anagrams": '''function groupAnagrams(strs) {
  const groups = new Map();
  for (const word of strs) {
    const key = Array.from(word).sort().join("");
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(word);
  }
  return Array.from(groups.values());
}''',
"longest_substring": '''function lengthOfLongestSubstring(s) {
  const lastSeen = new Map();
  let left = 0;
  let best = 0;
  for (let right = 0; right < s.length; right += 1) {
    const char = s[right];
    if (lastSeen.has(char) && lastSeen.get(char) >= left) {
      left = lastSeen.get(char) + 1;
    }
    lastSeen.set(char, right);
    best = Math.max(best, right - left + 1);
  }
  return best;
}''',
"product_except_self": '''function productExceptSelf(nums) {
  const result = new Array(nums.length).fill(1);
  let prefix = 1;
  for (let i = 0; i < nums.length; i += 1) {
    result[i] = prefix;
    prefix *= nums[i];
  }
  let suffix = 1;
  for (let i = nums.length - 1; i >= 0; i -= 1) {
    result[i] *= suffix;
    suffix *= nums[i];
  }
  return result;
}''',
"top_k_frequent": '''function topKFrequent(nums, k) {
  const counts = new Map();
  for (const value of nums) counts.set(value, (counts.get(value) || 0) + 1);
  const buckets = Array.from({ length: nums.length + 1 }, () => []);
  for (const [value, count] of counts) buckets[count].push(value);
  const result = [];
  for (let count = buckets.length - 1; count > 0; count -= 1) {
    for (const value of buckets[count]) {
      result.push(value);
      if (result.length === k) return result;
    }
  }
  return result;
}''',
"number_of_islands": '''function numIslands(grid) {
  if (grid.length === 0 || grid[0].length === 0) return 0;
  const rows = grid.length;
  const cols = grid[0].length;
  let islands = 0;
  for (let r = 0; r < rows; r += 1) {
    for (let c = 0; c < cols; c += 1) {
      if (grid[r][c] !== "1") continue;
      islands += 1;
      const stack = [[r, c]];
      grid[r][c] = "0";
      while (stack.length) {
        const [x, y] = stack.pop();
        for (const [nx, ny] of [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]) {
          if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && grid[nx][ny] === "1") {
            grid[nx][ny] = "0";
            stack.push([nx, ny]);
          }
        }
      }
    }
  }
  return islands;
}''',
"coin_change": '''function coinChange(coins, amount) {
  const dp = new Array(amount + 1).fill(amount + 1);
  dp[0] = 0;
  for (let value = 1; value <= amount; value += 1) {
    for (const coin of coins) {
      if (coin <= value) dp[value] = Math.min(dp[value], dp[value - coin] + 1);
    }
  }
  return dp[amount] <= amount ? dp[amount] : -1;
}''',
"climbing_stairs": '''function climbStairs(n) {
  if (n <= 2) return n;
  let one = 1;
  let two = 2;
  for (let step = 3; step <= n; step += 1) {
    const next = one + two;
    one = two;
    two = next;
  }
  return two;
}''',
"merge_intervals": '''function mergeIntervals(intervals) {
  if (intervals.length === 0) return [];
  const sorted = intervals.map(([start, end]) => [start, end]).sort((a, b) => a[0] - b[0]);
  const merged = [sorted[0]];
  for (const [start, end] of sorted.slice(1)) {
    const last = merged[merged.length - 1];
    if (start <= last[1]) last[1] = Math.max(last[1], end);
    else merged.push([start, end]);
  }
  return merged;
}''',
"linked_list_cycle": '''function hasCycle(head) {
  let slow = head;
  let fast = head;
  while (fast !== null && fast.next !== null) {
    slow = slow.next;
    fast = fast.next.next;
    if (slow === fast) return true;
  }
  return false;
}''',
"kth_largest": '''function findKthLargest(nums, k) {
  const heap = [];
  const push = (value) => {
    heap.push(value);
    let index = heap.length - 1;
    while (index > 0) {
      const parent = Math.floor((index - 1) / 2);
      if (heap[parent] <= heap[index]) break;
      [heap[parent], heap[index]] = [heap[index], heap[parent]];
      index = parent;
    }
  };
  const pop = () => {
    const root = heap[0];
    const last = heap.pop();
    if (heap.length) {
      heap[0] = last;
      let index = 0;
      while (true) {
        const left = index * 2 + 1;
        const right = left + 1;
        let smallest = index;
        if (left < heap.length && heap[left] < heap[smallest]) smallest = left;
        if (right < heap.length && heap[right] < heap[smallest]) smallest = right;
        if (smallest === index) break;
        [heap[index], heap[smallest]] = [heap[smallest], heap[index]];
        index = smallest;
      }
    }
    return root;
  };
  for (const value of nums) {
    push(value);
    if (heap.length > k) pop();
  }
  return heap[0];
}''',
"implement_trie": '''class TrieNode {
  constructor() {
    this.children = new Map();
    this.isEnd = false;
  }
}

class Trie {
  constructor() {
    this.root = new TrieNode();
  }

  insert(word) {
    let node = this.root;
    for (const char of word) {
      if (!node.children.has(char)) node.children.set(char, new TrieNode());
      node = node.children.get(char);
    }
    node.isEnd = true;
  }

  search(word) {
    const node = this.walk(word);
    return node !== null && node.isEnd;
  }

  startsWith(prefix) {
    return this.walk(prefix) !== null;
  }

  walk(text) {
    let node = this.root;
    for (const char of text) {
      if (!node.children.has(char)) return null;
      node = node.children.get(char);
    }
    return node;
  }
}'''
}

EXAMPLES = {
"two-sum":("nums = [2, 7, 11, 15], target = 9","[0, 1]"),
"valid-parentheses":("s = \"{[]}\"","true"),
"reverse-linked-list":("1 -> 2 -> 3 -> null","3 -> 2 -> 1 -> null"),
"merge-two-sorted-lists":("list1 = [1, 2, 4], list2 = [1, 3, 4]","[1, 1, 2, 3, 4, 4]"),
"maximum-subarray":("nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]","6, কারণ [4, -1, 2, 1]-এর sum 6"),
"binary-search":("nums = [-1, 0, 3, 5, 9, 12], target = 9","4"),
"best-time-to-buy-sell-stock":("prices = [7, 1, 5, 3, 6, 4]","5, price 1-এ buy এবং 6-এ sell"),
"contains-duplicate":("nums = [1, 2, 3, 1]","true"),
"valid-anagram":("s = \"anagram\", t = \"nagaram\"","true"),
"group-anagrams":("[\"eat\", \"tea\", \"tan\", \"ate\", \"nat\", \"bat\"]","[[\"eat\", \"tea\", \"ate\"], [\"tan\", \"nat\"], [\"bat\"]]"),
"longest-substring-without-repeating-characters":("s = \"abcabcbb\"","3, longest substring হলো \"abc\""),
"product-of-array-except-self":("nums = [1, 2, 3, 4]","[24, 12, 8, 6]"),
"top-k-frequent-elements":("nums = [1, 1, 1, 2, 2, 3], k = 2","[1, 2]"),
"number-of-islands":("grid = [[\"1\",\"1\",\"0\"],[\"1\",\"0\",\"0\"],[\"0\",\"0\",\"1\"]]","2"),
"coin-change":("coins = [1, 2, 5], amount = 11","3, কারণ 5 + 5 + 1"),
"climbing-stairs":("n = 4","5"),
"merge-intervals":("intervals = [[1,3],[2,6],[8,10],[15,18]]","[[1,6],[8,10],[15,18]]"),
"linked-list-cycle":("3 -> 2 -> 0 -> -4, শেষ node-এর next দ্বিতীয় node-কে point করে","true"),
"kth-largest-element":("nums = [3, 2, 1, 5, 6, 4], k = 2","5"),
"implement-trie":("insert(\"apple\"), search(\"apple\"), search(\"app\"), startsWith(\"app\")","true, false, true")
}

CATEGORY_LABELS = {
"dsa":"DSA & Algorithms","system-design":"System Design","database":"Database","behavioral":"Behavioral","languages":"Languages & Runtime","bangladesh":"Bangladesh Interviews"
}

def bullet_lines(items):
    return "\n".join(f"- {x}" for x in items)

def dsa_body(q):
    a, o = EXAMPLES.get(q["slug"], ("Input example","Expected output"))
    key = q["custom"]["codekey"]
    py = PY_SOLUTIONS[key]
    js = JS_SOLUTIONS[key]
    notes = {
        "two_sum":"প্রতি সংখ্যাকে দেখার সময় কেবল আগে দেখা value-তে complement খোঁজা হয়। Current value আগে map-এ রাখলে একই index দুবার ব্যবহারের ঝুঁকি তৈরি হতো, তাই lookup আগে।",
        "valid_parentheses":"Stack-এর top-ই সর্বশেষ unmatched opening bracket। Closing bracket-এর type top-এর সঙ্গে না মিললে আর কোনো ভবিষ্যৎ character সেটি ঠিক করতে পারবে না, তাই সঙ্গে সঙ্গে false।",
        "reverse-linked-list":"একটি link বদলানোর আগেই পরের node pointer-এ save করি। এভাবে কোনো node হারায় না, এবং input nodes-ই reuse হয়।",
        "merge_two_sorted_lists":"দুই list sorted হওয়ায় তাদের head-এর ছোট node-টিই পুরো অবশিষ্ট অংশের সবচেয়ে ছোট candidate। Dummy node প্রথম insertion-এর special case বাদ দেয়।",
        "maximum_subarray":"প্রতিটি position-এ শেষ হওয়া সেরা subarray-এর sum রাখি। আগের running sum negative হলে current value দিয়ে নতুন subarray শুরু করা ভালো।",
        "binary_search":"প্রতিটি comparison-এ অর্ধেক search interval বাদ যায়। Loop condition low <= high একটিমাত্র সম্ভাব্য index-ও পরীক্ষা করতে দেয়।",
        "best_time_stock":"প্রতিটি sell day-তে আগের সবচেয়ে কম price-টি buy হিসেবে ব্যবহার করলে সেই day-র সর্বোচ্চ profit পাওয়া যায়। Global best শুধু বাড়াই।",
        "contains_duplicate":"Set membership একটি value আগে দেখা হয়েছে কি না দ্রুত জানায়। Duplicate পাওয়া মাত্র early return করা যায়।",
        "valid_anagram":"Counter/frequency map character count তুলনা করে; কেবল unique character বা sortedness নয়, প্রতিটি character-এর multiplicity গুরুত্বপূর্ণ।",
        "group_anagrams":"একই character-গুলো ভিন্ন order-এ থাকলেও sorted canonical key একই হয়। Key একই হলে string-গুলো একই group-এ যায়।",
        "longest_substring":"`last_seen` map প্রতিটি character-এর recent index রাখে। Left pointer কখনো পিছনে যায় না, তাই প্রত্যেক index সর্বোচ্চ কয়েকবার process হয়।",
        "product_except_self":"Result প্রথমে prefix product দিয়ে পূরণ হয়। দ্বিতীয় pass suffix product গুণ করে; division নেই বলে zero-র case আলাদা করতে হয় না।",
        "top_k_frequent":"Frequency অনুযায়ী bucket বানালে frequency sort করতে হয় না। সবচেয়ে বেশি count থেকে bucket scan করে kটি distinct value সংগ্রহ করি।",
        "number_of_islands":"প্রতিটি unseen land cell একটি নতুন island শুরু করে। DFS চলাকালে cell-কে water হিসেবে mark করায় সেটি দ্বিতীয়বার count হবে না।",
        "coin_change":"DP-তে amount a-এর উত্তর ছোট amount a-coin-এর উত্তর থেকে পাওয়া যায়। Impossible amount sentinel value-তে থাকে এবং শেষে -1-এ map হয়।",
        "climbing_stairs":"শেষ ধাপের আগের অবস্থান n-1 বা n-2; তাই দুইটি আগের count যোগ হয়। কেবল দুইটি state রাখায় extra space constant।",
        "merge_intervals":"Sort করার পর সব সম্ভাব্য overlap বর্তমান last interval-এর সঙ্গে তুলনা করলেই বোঝা যায়। End point-এর maximum নিয়ে merged range বাড়াই।",
        "linked_list_cycle":"Fast pointer দুই step, slow এক step চলে। Cycle না থাকলে fast null-এ পৌঁছায়; cycle থাকলে relative distance একসময় শূন্য হয়।",
        "kth_largest":"Size k min-heap-এ এ পর্যন্ত দেখা kটি বৃহত্তম value থাকে। Heap top এই kটির মধ্যে সবচেয়ে ছোট, তাই সেটিই kth largest।",
        "implement_trie":"প্রতি node-এ child map এবং isEnd flag থাকে। Prefix path পাওয়া আর full word inserted থাকা আলাদা বিষয়, তাই terminal flag দরকার।"
    }
    return f'''## Problem

{q['problem']}

## Example

**Input:** `{a}`

**Output:** `{o}`

## Approach বাংলায়

{q['approach']}

{notes.get(key, q['back'])}

## Python solution

```python
{py}
```

## JavaScript solution

```javascript
{js}
```

## Complexity analysis

- **Time:** {q['complexity']['time']} — প্রতিটি item কতবার process হয় এবং sorting/heap থাকলে তার cost হিসাব করো।
- **Extra space:** {q['complexity']['space']} — input বাদে তৈরি করা auxiliary structure-এর ব্যবহার এই হিসাবে ধরা হয়েছে।

## Edge cases

{bullet_lines(q['edges'])}

## Interview follow-up

প্রথমে brute-force approach এবং তার complexity ব্যাখ্যা করো, তারপর optimized approach কেন কাজ করে তার invariant বলো। এরপর input size, duplicate, empty input এবং worst-case memory নিয়ে interviewer-এর সঙ্গে কথা বলো।

## Related practice

এই pattern আরও ভালো বোঝার জন্য related question-গুলো করো: {', '.join(q['related'])}।
'''

def system_body(q):
    slug = q['slug']
    extra = {
        "url-shortener":"Code generation-এ random/base62 identifier collision check বা database unique constraint দরকার। Redirect endpoint-এ short code cache করা যায়, আর click analytics asynchronous event হিসেবে পাঠালে redirect latency কম থাকে।",
        "rate-limiter":"Policy evaluation endpoint, API key/user identity, limit configuration এবং response headers-কে এক জায়গায় model করো। Redis Lua বা atomic operation এক request-এর token read-update-write sequence race-condition ছাড়া চালাতে পারে।",
        "chat-system":"Message ID client-side generated হতে পারে যাতে retry deduplicate হয়। History API cursor-based pagination-এ message timestamp-এর পাশাপাশি stable ID tie-breaker রাখলে একই timestamp-এর message-ও deterministic order পায়।",
        "news-feed":"Ranking ও candidate generation আলাদা রাখলে ranking model বদলালেও graph-storage layer পাল্টাতে হয় না। Feed entry-তে post ID রাখলে deletion, privacy এবং freshness check post service-এ প্রয়োগ করা যায়।",
        "file-storage":"Metadata commit এবং object upload-এর lifecycle state স্পষ্ট রাখো: pending, uploaded, scanning, ready, failed। Upload complete না হলে download URL প্রকাশ কোরো না।",
        "notification-system":"Delivery status attempt-level এ রাখলে provider retry ও fallback channel auditable হয়। Dead-letter queue-র message manual replay করার আগে consent, template version ও idempotency key পুনরায় যাচাই করতে হয়।",
        "ride-sharing":"Driver search-এর radius বাড়ানো, ETA estimate cache এবং dispatch lease expiry দিয়ে throughput ও matching quality balance করা যায়। GPS update stale হলে candidate বাদ দেওয়ার rule স্পষ্ট থাকতে হবে।",
        "video-streaming":"Original upload-কে immutable object key দাও; transcoded outputs versioned path-এ রাখলে partial retry ও CDN cache management সহজ হয়। Encoding job state event-driven রাখো।",
        "ecommerce-checkout":"Order state transition-কে explicit state machine হিসেবে define করো: pending, reserved, authorized, confirmed, cancelled, refunded। Provider webhook duplicate বা out-of-order হতে পারে, তাই signature verify ও current-state check প্রয়োজন।",
        "search-autocomplete":"Query logs থেকে user-identifying data বাদ দিয়ে popularity aggregate করো। Prefix suggestion cache-এ locale, language এবং personalization scope key-এর অংশ হতে পারে।"
    }
    api = {
        "url-shortener":"POST /api/links creates a mapping; GET /{code} redirects; GET /api/links/{code}/stats returns authorized analytics.",
        "rate-limiter":"Gateway evaluates identity and policy before forwarding; a rejection can return HTTP 429 and Retry-After.",
        "chat-system":"POST /conversations/{id}/messages sends a message; GET /conversations/{id}/messages?cursor=... fetches history; WebSocket delivers live events.",
        "news-feed":"POST /posts creates content; GET /feed?cursor=... returns ranked entries; POST /follows changes graph edges.",
        "file-storage":"POST /uploads creates an upload session; POST /uploads/{id}/complete finalizes it; GET /files/{id} checks permission before issuing a download URL.",
        "notification-system":"POST /events adds a business event; GET /notifications lists in-app items; preference APIs manage channel consent.",
        "ride-sharing":"POST /rides creates a request; POST /rides/{id}/accept performs an atomic driver claim; location updates feed the geospatial index.",
        "video-streaming":"POST /videos creates an upload session; GET /videos/{id}/manifest returns playback manifest after processing; webhooks report transcoding state.",
        "ecommerce-checkout":"POST /checkout accepts an idempotency key; GET /orders/{id} returns order state; POST /payments/webhook handles signed provider events.",
        "search-autocomplete":"GET /suggest?q=prefix&limit=10 returns top suggestions; analytics ingestion is asynchronous and independent of the suggestion request."
    }
    return f'''## Problem and scope

{q['problem']}

সিস্টেম design শুরু করার আগে interviewer-এর সঙ্গে scope ঠিক করো। এখানে মূল user journey-টি হলো: request authenticate/validate করা, durable state পরিবর্তন করা, response দেওয়া, এবং asynchronous কাজ থাকলে তা নির্ভরযোগ্যভাবে শেষ করা।

## Functional and non-functional requirements

Functional requirement হিসেবে {q['topic'].lower()}-এর প্রধান user action এবং তার failure/unauthorized case cover করতে হবে। Non-functional দিক থেকে latency, throughput, availability, data durability, privacy এবং operational cost-এর মধ্যে কোনটি priority তা পরিষ্কার করে নাও। Interview-তে সংখ্যাগত traffic না দেওয়া হলে read/write ratio, peak traffic, data retention ও regional scope সম্পর্কে reasonable assumption স্পষ্টভাবে বলো—কল্পিত metric-কে fact হিসেবে উপস্থাপন কোরো না।

## High-level architecture

{q['approach']}

Typical request flow-এ CDN/load balancer বা API gateway request গ্রহণ করে, stateless application service authentication ও business rule প্রয়োগ করে, primary database durable state রাখে এবং cache repeated read accelerate করে। Queue/stream slow side effect-কে synchronous request থেকে আলাদা করে। Service boundary-গুলো product requirement অনুযায়ী রাখো; diagram-এ অপ্রয়োজনীয় microservice বাড়ানোর বদলে প্রথমে simplest reliable design ব্যাখ্যা করো।

## API contract

একটি সম্ভাব্য interface:

```text
{api[slug]}
```

Request validate করতে হবে, error response stable রাখতে হবে এবং create/side-effect operation retry হলে কী হবে তা সংজ্ঞায়িত করতে হবে। Mutation endpoint-এ idempotency key বা version check যেখানে দরকার ব্যবহার করো। API response-এ internal stack trace বা secret প্রকাশ করা যাবে না।

## Data model and storage

প্রধান durable entities: {q['complexity']['space']}। Storage-এ stable primary key, ownership/permission, created/updated timestamps এবং query pattern অনুযায়ী index রাখো। Read-heavy অংশ cache করা গেলেও canonical state কোথায় থাকে তা একটি authoritative store-এ স্পষ্ট হওয়া দরকার। Retention, deletion এবং audit requirements data model-এর অংশ।

## Scaling strategy

প্রথমে horizontal stateless scale, query/index tuning, bounded pagination এবং cache ব্যবহার করো। Traffic একটি key, tenant বা creator-এ কেন্দ্রীভূত হলে sharding বা fan-out strategy-এর skew বিবেচনা করতে হবে। Queue backlog, database connection saturation এবং p95/p99 latency-কে capacity signal হিসেবে ধরো; কেবল average latency যথেষ্ট নয়।

## Reliability, security, and failure modes

{extra[slug]}

Timeout, retry, exponential backoff with jitter এবং circuit breaking দরকার হতে পারে, কিন্তু retry idempotency ছাড়া duplicate effect তৈরি করতে পারে। Authentication ছাড়াও resource-level authorization, rate limiting, secret management, audit logs ও data minimization design-এর অন্তর্ভুক্ত। Dependency down থাকলে fail-open না fail-closed হবে তা business impact অনুযায়ী নির্ধারণ করো।

## Trade-offs to discuss

{q['edges'][0]} {q['edges'][1]} {q['edges'][2]} এগুলো design review-তে আগে থেকেই ধরো। Strong consistency, lower latency, implementation complexity এবং cost একসঙ্গে সর্বোত্তম করা যায় না; কোন trade-off বেছে নিয়েছ এবং কোন metric দেখে পরে revisit করবে তা বলতে হবে।

## Interview walkthrough

প্রথম 2–3 মিনিট clarification ও capacity assumptions, পরের অংশ API/data model, তারপর architecture ও main data flow, শেষে failure handling এবং bottleneck দিয়ে শেষ করো। পরিষ্কার diagram এবং নিজের assumption উচ্চস্বরে ব্যাখ্যা করা মুখস্থ component list বলার চেয়ে বেশি কার্যকর।
'''

def database_body(q):
    slug=q['slug']
    examples = {
        "database-indexes":"ধরা যাক `orders` table-এ customer-এর recent order খুঁজতে `WHERE customer_id = ? ORDER BY created_at DESC LIMIT 20` query চলে। `(customer_id, created_at)` composite index এই query-র access path-এ সাহায্য করতে পারে; final decision execution plan এবং real data distribution দেখে নাও।",
        "acid-transactions":"Money transfer-এ source account debit ও destination account credit একই transaction-এ করো। দুই operation-এর যেকোনোটি fail করলে rollback হবে; account balance-এর invariant database constraints ও business logic দিয়ে রক্ষা করতে হবে।",
        "sql-joins":"`customers` থেকে সব customer এবং থাকলে তাদের order দেখাতে `LEFT JOIN orders ON orders.customer_id = customers.id` ব্যবহার করা যায়। Order না থাকলে order columns NULL হবে; WHERE clause-এ সেগুলো mandatory করলে unmatched customer বাদ পড়ে যেতে পারে।",
        "database-normalization":"একটি order row-তে customer address প্রতিবার copy করলে customer address বদলালে বহু order update করতে হবে। Customer profile আলাদা table-এ রাখলে single source of truth পাওয়া যায়; historical shipping snapshot দরকার হলে সেটি আলাদা business rule হিসেবে রাখো।",
        "transactions-and-locking":"দুই transaction একই account balance পড়েই debit করলে lost update হতে পারে। Atomic conditional update, row lock বা appropriate isolation ব্যবহার করো এবং conflict হলে bounded retry করো।"
    }
    return f'''## Core concept

{q['problem']}

## Explanation বাংলায়

{q['approach']}

## Practical example

{examples[slug]}

## কীভাবে verify করবে

একটি ছোট reproducible dataset দিয়ে expected output পরীক্ষা করো। Database-এ `EXPLAIN`/`EXPLAIN ANALYZE` বা সমতুল্য query plan দেখো, কিন্তু production data-তে expensive analysis চালানোর আগে impact বুঝে নাও। Performance-এর সিদ্ধান্ত শুধু table row count দিয়ে নয়, selectivity, access pattern, transaction contention এবং write volume দেখে নেওয়া উচিত।

## Trade-offs and edge cases

{bullet_lines(q['edges'])}

Interview-তে কোনো feature-এর নাম বলার পাশাপাশি failure mode ব্যাখ্যা করো: NULL কী করে, duplicate key থাকলে কী হয়, concurrent transaction কীভাবে interact করে এবং retry safe কি না।

## Related concepts

{', '.join(q['related'])} — এগুলো একসঙ্গে পড়লে indexing, data model এবং correctness-এর সম্পর্ক স্পষ্ট হবে।
'''

def behavioral_body(q):
    star=q['custom']['star']
    return f'''## Interview prompt

{q['problem']}

## কেন interviewer প্রশ্নটি করেন

এটি শুধু story শোনার প্রশ্ন নয়। Interviewer দেখতে চান তুমি context পরিষ্কার করতে পারো কি না, নিজের responsibility চেনো কি না, action নেওয়ার সময় কীভাবে সিদ্ধান্ত নিয়েছ এবং ফলাফল থেকে কী শিখেছ।

## STAR framework

**S — Situation:** {star['situation']}

**T — Task:** {star['task']}

**A — Action:** {star['action']}

**R — Result:** {star['result']}

উপরের উত্তরটি একটি কাঠামোগত নমুনা। এটিকে নিজের বাস্তব অভিজ্ঞতার সঙ্গে মানিয়ে নাও; কোনো ঘটনা না ঘটলে সেটি নিজের জীবনের ঘটনা বলে দাবি না করে কাছাকাছি project example বা hypothetical approach স্পষ্টভাবে বলো। Result-এ পরিমাপযোগ্য evidence থাকলে ব্যবহার করো, কিন্তু সংখ্যা বানিয়ে বলো না।

## Strong answer checklist

{bullet_lines(q['edges'])}

## Practice version

নিজের উত্তর 60–120 সেকেন্ডে রেকর্ড করে শুনো। Situation ও Task সংক্ষিপ্ত রাখো; Action অংশে “আমি কী সিদ্ধান্ত নিয়েছিলাম” পরিষ্কার করো; Result-এ কী deliver হয়েছে, কার উপকার হয়েছে এবং পরেরবার কী বদলাবে তা বলো।
'''

def language_body(q):
    slug=q['slug']
    code = {
        "python-list-vs-tuple":('python','''items = ["a", "b"]
items.append("c")

point = (10, 20)

record = {"name": "Fahim", "skills": ["Python"]}
record["skills"].append("SQL")''','এখানে list-এর structure mutate করা যায়; tuple-এর element binding পরিবর্তন করা যায় না, কিন্তু tuple-এর মধ্যে থাকা mutable object এখনও mutate হতে পারে।'),
        "javascript-event-loop":('javascript','''console.log("start");
setTimeout(() => console.log("timer"), 0);
Promise.resolve().then(() => console.log("promise"));
console.log("end");''','সাধারণ browser runtime-এ output order: start, end, promise, timer। Synchronous log আগে হয়, Promise callback microtask, timer callback পরে task হিসেবে চলে।'),
        "javascript-closures":('javascript','''function makeCounter() {
  let count = 0;
  return function increment() {
    count += 1;
    return count;
  };
}

const counter = makeCounter();
console.log(counter());
console.log(counter());''','Returned function `count` binding ধরে রাখে; outer call শেষ হলেও পরবর্তী call-এ আগের state থাকে।'),
        "typescript-type-vs-interface":('typescript','''type Result<T> = { data: T } | { error: string };

interface User {
  id: string;
  displayName: string;
}

const result: Result<User> = { data: { id: "u1", displayName: "Fahim" } };''','Union-এর জন্য type alias স্বাভাবিক; object contract-এর জন্য interface-ও উপযুক্ত। এই annotation runtime-এ untrusted JSON validate করে না।'),
        "python-gil":('python','''from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen

def fetch(url):
    with urlopen(url, timeout=5) as response:
        return response.status

urls = ["https://example.com"]
with ThreadPoolExecutor(max_workers=4) as pool:
    statuses = list(pool.map(fetch, urls))''','Network wait-এর সময়ে thread অন্য কাজ করতে পারে। CPU-bound pure Python কাজের জন্য workload অনুযায়ী multiprocessing বা native/vectorized library বিবেচনা করো।'),
        "javascript-async":('javascript','''async function loadDashboard() {
  const [profileResponse, statsResponse] = await Promise.all([
    fetch("/api/profile"),
    fetch("/api/stats")
  ]);
  if (!profileResponse.ok || !statsResponse.ok) {
    throw new Error("Dashboard request failed");
  }
  return Promise.all([profileResponse.json(), statsResponse.json()]);
}''','দুইটি independent fetch একসঙ্গে শুরু হয়। Response status check, exception handling এবং প্রয়োজন হলে AbortController দিয়ে cancellation যোগ করতে হবে।'),
        "memory-garbage-collection":('javascript','''const cache = new Map();

function remember(key, value) {
  cache.set(key, value);
}

function forget(key) {
  cache.delete(key);
}''','Long-lived cache limit না থাকলে সব key জমতে পারে। TTL, LRU eviction বা explicit deletion retention control করতে পারে।'),
        "javascript-this":('javascript','''const user = {
  name: "Fahim",
  showName() {
    return this.name;
  }
};

const show = user.showName;
console.log(user.showName());
console.log(show());''','প্রথম call-এ receiver `user`; detached regular function-এ strict mode-এ `this` undefined হতে পারে। Callback হিসেবে ব্যবহার করতে চাইলে bind বা arrow closure context বুঝে বেছে নাও।'),
        "api-error-handling":('typescript','''type ApiError = {
  code: string;
  message: string;
  requestId: string;
};

function conflictError(requestId: string): ApiError {
  return {
    code: "RESOURCE_CONFLICT",
    message: "The resource changed. Refresh and try again.",
    requestId
  };
}''','Error response-এ stable code ও request ID client support/debugging-এ সহায়তা করে। Internal exception details server-side structured logs-এ রাখো।'),
        "http-caching":('http','''Cache-Control: public, max-age=31536000, immutable
ETag: "asset-v3-a83f"

If-None-Match: "asset-v3-a83f"''','Fingerprint URL-সহ versioned static asset দীর্ঘদিন cache করা যায়। ETag validator দিয়ে stale response revalidation করা যায়; personalized data public cache করা উচিত নয়।')
    }
    lang, snippet, explanation = code[slug]
    return f'''## Interview prompt

{q['problem']}

## Explanation বাংলায়

{q['approach']}

## Example

```{lang}
{snippet}
```

{explanation}

## Common mistakes

{bullet_lines(q['edges'])}

## Interview-ready answer

প্রথমে concept-টি এক বা দুই বাক্যে সংজ্ঞায়িত করো। তারপর code/runtime-এর ছোট example, trade-off এবং একটি failure case বলো। Performance claim করলে কোন runtime/version বা workload ধরে বলছ তা স্পষ্ট করো; implementation-specific behavior-কে সব language-এর নিয়ম হিসেবে উপস্থাপন কোরো না।

## Related concepts

{', '.join(q['related'])}
'''

def bangladesh_body(q):
    slug=q['slug']
    sample = {
        "bd-self-introduction":"আমি web development-এ focus করছি এবং frontend, API integration ও responsive UI নিয়ে hands-on project করেছি। একটি project-এ আমার কাজ ছিল [নিজের feature]-এর implementation, testing এবং bug fixing। এখন এমন team-এ কাজ করতে চাই যেখানে maintainable software ship করার পাশাপাশি code review থেকে শিখতে পারব।",
        "bd-salary-expectation":"এই role-এর scope, benefits এবং review cycle বুঝে একটি fair range নিয়ে আলোচনা করতে আগ্রহী। আমার expectation হলো [research করা range], তবে responsibilities এবং total compensation package জানলে আরও নির্দিষ্টভাবে বলতে পারব।",
        "bd-notice-period":"আমার current commitment ও applicable notice policy verify করে নির্দিষ্ট joining date দিতে পারব। Handover এবং documentation দায়িত্ব নিয়ে শেষ করতে চাই, যাতে transition smooth থাকে।",
        "bd-remote-work":"আমি task ও blocker লিখিতভাবে update করতে, কাজকে ছোট deliverable-এ ভাঙতে এবং timezone overlap আগে agree করতে পছন্দ করি। Remote কাজের জন্য secure account access, documented handoff এবং predictable status update বজায় রাখব।",
        "bd-junior-experience-gap":"আমার professional experience এখনও সীমিত, তাই যে কাজ করেছি তার evidence দেখাতে চাই। আমি [নিজের project]-এ [নিজের contribution] করেছি, debugging ও testing-এর বিষয়গুলো ব্যাখ্যা করতে পারব, এবং যে area-তে production exposure কম সেটি দ্রুত শেখার plan আছে।"
    }
    return f'''## Interview prompt

{q['problem']}

## বাংলায় প্রস্তুতি

{q['approach']}

## Sample answer

> {sample[slug]}

এই নমুনার square-bracket অংশগুলো নিজের সত্য তথ্য দিয়ে বদলাও। ভিন্ন ভাষায় interview হলেও answer-এর core message একই রাখো এবং technical term প্রয়োজনমতো English-এ ব্যবহার করো।

## Bangladesh-specific checklist

{bullet_lines(q['edges'])}

## Follow-up questions প্রস্তুত করো

Interviewer যদি “একটি উদাহরণ দাও”, “কেন এমন সিদ্ধান্ত নিলে?” বা “আবার করলে কী বদলাবে?” জিজ্ঞেস করেন, তখন claim-এর সঙ্গে বাস্তব project, document, test, communication বা decision-এর evidence দেখাও। Salary, joining date বা experience-এর ক্ষেত্রে যাচাই করা তথ্যই বলো।

## Related practice

{', '.join(q['related'])}
'''

def body_for(q):
    if q['category']=='dsa': return dsa_body(q)
    if q['category']=='system-design': return system_body(q)
    if q['category']=='database': return database_body(q)
    if q['category']=='behavioral': return behavioral_body(q)
    if q['category']=='languages': return language_body(q)
    return bangladesh_body(q)

FILES = {
"package.json": r'''{
  "name": "interviewprep-bd",
  "version": "1.0.0",
  "private": true,
  "description": "Free Bengali and English coding interview preparation by RA Fahim.",
  "scripts": {
    "dev": "next dev",
    "predev": "npm run generate:sitemap",
    "build": "next build",
    "prebuild": "npm run generate:sitemap",
    "start": "next start",
    "generate:sitemap": "node scripts/generate-sitemap.mjs",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "@supabase/supabase-js": "^2.45.4",
    "fuse.js": "^7.0.0",
    "gray-matter": "^4.0.3",
    "next": "14.2.31",
    "next-mdx-remote": "^5.0.0",
    "react": "18.3.1",
    "react-dom": "18.3.1",
    "rehype-pretty-code": "^0.14.0",
    "shiki": "^1.22.2"
  },
  "devDependencies": {
    "@types/node": "^20.14.10",
    "@types/react": "^18.3.3",
    "@types/react-dom": "^18.3.0",
    "autoprefixer": "^10.4.20",
    "postcss": "^8.4.41",
    "tailwindcss": "^3.4.14",
    "typescript": "^5.5.4"
  }
}''',
"next.config.js": r'''const nextConfig = {
  basePath: "/interview-prep",
  trailingSlash: true,
  poweredByHeader: false,
  images: { unoptimized: true },
  reactStrictMode: true
};

module.exports = nextConfig;''',
"postcss.config.js": r'''module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {}
  }
};''',
"tailwind.config.ts": r'''import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: ["./app/**/*.{js,ts,jsx,tsx,mdx}", "./components/**/*.{js,ts,jsx,tsx,mdx}", "./lib/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        ink: "#070a12",
        panel: "#0e1422",
        line: "#202a3d",
        mint: "#75f0c1",
        sky: "#86bfff",
        amber: "#f5c76b"
      },
      boxShadow: {
        glow: "0 0 60px rgba(117, 240, 193, 0.08)"
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"]
      }
    }
  },
  plugins: []
};

export default config;''',
"tsconfig.json": r'''{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "es2022"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./*"] }
  },
  "include": ["next-env.d.ts", ".next/types/**/*.ts", "**/*.ts", "**/*.tsx"],
  "exclude": ["node_modules"]
}''',
".gitignore": r'''node_modules/
.next/
out/
coverage/
.env
.env.local
.env.*.local
*.log
.DS_Store
*.zip
.vercel/
*.tsbuildinfo''',
".env.example": r'''NEXT_PUBLIC_SITE_URL=https://rafahim.com/interview-prep
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
NEXT_PUBLIC_GISCUS_REPO=rafahim/interviewprep-bd
NEXT_PUBLIC_GISCUS_REPO_ID=
NEXT_PUBLIC_GISCUS_CATEGORY=General
NEXT_PUBLIC_GISCUS_CATEGORY_ID=''' ,
"types/index.ts": r'''export type Difficulty = "Easy" | "Medium" | "Hard";
export type ProgressStatus = "todo" | "in-progress" | "solved" | "needs-review";
export type QuestionCategory = "dsa" | "system-design" | "database" | "behavioral" | "languages" | "bangladesh";

export type FlashcardData = {
  front: string;
  back: string;
};

export type QuestionMeta = {
  slug: string;
  title: string;
  category: QuestionCategory;
  topic: string;
  difficulty: Difficulty;
  companies: string[];
  languages: string[];
  frequency: "High" | "Medium" | "Low";
  minutes: number;
  problem: string;
  approach: string;
  complexity: { time: string; space: string };
  edges: string[];
  related: string[];
  front: string;
  back: string;
  summary: string;
  tags: string[];
  examples: { input: string; output: string };
  order: number;
};

export type Question = QuestionMeta & { content: string };
export type QuestionIndexItem = Omit<Question, "content">;

export type ProgressRecord = {
  status: ProgressStatus;
  updatedAt: string;
  repetitions: number;
  interval: number;
  easeFactor: number;
  nextReview: string | null;
  lastRating?: number;
};

export type ProgressMap = Record<string, ProgressRecord>;
''',
"lib/categories.ts": r'''import type { QuestionCategory } from "@/types";

export const CATEGORY_LABELS: Record<QuestionCategory, string> = {
  dsa: "DSA & Algorithms",
  "system-design": "System Design",
  database: "Database",
  behavioral: "Behavioral",
  languages: "Languages & Runtime",
  bangladesh: "Bangladesh Interviews"
};

export const CATEGORY_DESCRIPTIONS: Record<QuestionCategory, string> = {
  dsa: "Arrays, graphs, linked lists, dynamic programming and core patterns.",
  "system-design": "Design reliable systems, APIs, storage, queues and distributed services.",
  database: "SQL, indexes, transactions, normalization and database internals.",
  behavioral: "STAR-based examples for teamwork, ownership, feedback and growth.",
  languages: "Runtime behavior, async code, types, memory and language fundamentals.",
  bangladesh: "Practical interview preparation for Bangladesh and remote tech roles."
};

export const CATEGORY_ORDER: QuestionCategory[] = ["dsa", "system-design", "database", "behavioral", "languages", "bangladesh"];
''',
"lib/questions.ts": r'''import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import type { Question, QuestionIndexItem, QuestionMeta } from "@/types";

const CONTENT_DIR = path.join(process.cwd(), "content");
const CATEGORY_DIRS = ["dsa", "system-design", "database", "behavioral", "languages", "bangladesh"];

function getMdxFiles(dir: string): string[] {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const entryPath = path.join(dir, entry.name);
    if (entry.isDirectory()) return getMdxFiles(entryPath);
    return entry.isFile() && entry.name.endsWith(".mdx") ? [entryPath] : [];
  });
}

function readQuestion(filePath: string): Question {
  const source = fs.readFileSync(filePath, "utf8");
  const parsed = matter(source);
  const meta = parsed.data as QuestionMeta;
  if (!meta.slug || !meta.title || !meta.category) {
    throw new Error(`Missing required question frontmatter in ${filePath}`);
  }
  return { ...meta, content: parsed.content.trim() };
}

export function getAllQuestions(): Question[] {
  return CATEGORY_DIRS.flatMap((category) => getMdxFiles(path.join(CONTENT_DIR, category)))
    .map(readQuestion)
    .sort((a, b) => a.order - b.order || a.title.localeCompare(b.title));
}

export function getQuestionIndex(): QuestionIndexItem[] {
  return getAllQuestions().map(({ content, ...question }) => question);
}

export function getQuestionBySlug(slug: string): Question | undefined {
  const file = getAllQuestions().find((question) => question.slug === slug);
  return file;
}
''',
"lib/seo.ts": r'''import type { Metadata } from "next";

export const SITE_NAME = "InterviewPrep BD";
export const SITE_URL = "https://rafahim.com/interview-prep";
export const OWNER_URL = "https://rafahim.com";
export const DEFAULT_DESCRIPTION = "Free coding interview questions with Bengali explanations, Python and JavaScript solutions, system design, behavioral STAR answers and local interview guidance.";
export const KEYWORDS = ["interview prep", "coding interview", "bangla interview prep", "dsa practice", "system design"];

export function pageMetadata(title: string, description: string, route: string): Metadata {
  const canonical = `${SITE_URL}${route === "/" ? "/" : route.endsWith("/") ? route : `${route}/`}`;
  return {
    title,
    description,
    keywords: KEYWORDS,
    authors: [{ name: "RA Fahim", url: OWNER_URL }],
    creator: "RA Fahim",
    alternates: { canonical },
    openGraph: {
      type: "website",
      locale: "en_BD",
      url: canonical,
      siteName: SITE_NAME,
      title: `${title} | InterviewPrep BD by RA Fahim`,
      description,
      images: [{ url: `${SITE_URL}/og-image.svg`, width: 1200, height: 630, alt: "InterviewPrep BD by RA Fahim" }]
    },
    twitter: {
      card: "summary_large_image",
      creator: "@rafahimn",
      title: `${title} | InterviewPrep BD by RA Fahim`,
      description,
      images: [`${SITE_URL}/og-image.svg`]
    }
  };
}
''',
"lib/sm2.ts": r'''export type SM2State = {
  repetitions: number;
  interval: number;
  easeFactor: number;
  nextReview: string | null;
};

export function calculateSM2(previous: SM2State, rating: number, now = new Date()): SM2State {
  const quality = Math.max(0, Math.min(5, Math.round(rating)));
  let repetitions = previous.repetitions;
  let interval = previous.interval;
  let easeFactor = previous.easeFactor || 2.5;
  if (quality < 3) {
    repetitions = 0;
    interval = 1;
  } else {
    if (repetitions === 0) interval = 1;
    else if (repetitions === 1) interval = 6;
    else interval = Math.max(1, Math.round(interval * easeFactor));
    repetitions += 1;
  }
  easeFactor = Math.max(1.3, easeFactor + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02));
  const next = new Date(now);
  next.setDate(next.getDate() + interval);
  return { repetitions, interval, easeFactor, nextReview: next.toISOString() };
}''',
"lib/progress.ts": r'''import type { ProgressMap, ProgressRecord, ProgressStatus } from "@/types";
import { calculateSM2 } from "@/lib/sm2";

const PROGRESS_KEY = "ipbd.progress.v1";
const ACTIVITY_KEY = "ipbd.activity.v1";

export function readProgress(): ProgressMap {
  if (typeof window === "undefined") return {};
  try {
    return JSON.parse(window.localStorage.getItem(PROGRESS_KEY) || "{}") as ProgressMap;
  } catch {
    return {};
  }
}

export function readActivity(): string[] {
  if (typeof window === "undefined") return [];
  try {
    const value = JSON.parse(window.localStorage.getItem(ACTIVITY_KEY) || "[]");
    return Array.isArray(value) ? value.filter((item) => typeof item === "string") : [];
  } catch {
    return [];
  }
}

export function recordActivity(now = new Date()): void {
  if (typeof window === "undefined") return;
  const day = now.toISOString().slice(0, 10);
  const activity = new Set(readActivity());
  activity.add(day);
  window.localStorage.setItem(ACTIVITY_KEY, JSON.stringify([...activity].sort().slice(-365)));
}

export function saveStatus(slug: string, status: ProgressStatus): ProgressMap {
  const progress = readProgress();
  const current = progress[slug] || { status: "todo", updatedAt: new Date().toISOString(), repetitions: 0, interval: 0, easeFactor: 2.5, nextReview: null };
  progress[slug] = { ...current, status, updatedAt: new Date().toISOString() };
  if (status === "solved") {
    const next = calculateSM2(current, 4);
    progress[slug] = { ...progress[slug], ...next, lastRating: 4 };
  }
  if (typeof window !== "undefined") window.localStorage.setItem(PROGRESS_KEY, JSON.stringify(progress));
  recordActivity();
  return progress;
}

export function reviewQuestion(slug: string, rating: number): ProgressMap {
  const progress = readProgress();
  const current: ProgressRecord = progress[slug] || { status: "needs-review", updatedAt: new Date().toISOString(), repetitions: 0, interval: 0, easeFactor: 2.5, nextReview: null };
  const next = calculateSM2(current, rating);
  progress[slug] = { ...current, ...next, status: rating < 3 ? "needs-review" : "solved", lastRating: rating, updatedAt: new Date().toISOString() };
  if (typeof window !== "undefined") window.localStorage.setItem(PROGRESS_KEY, JSON.stringify(progress));
  recordActivity();
  return progress;
}

export function getCurrentStreak(activity = readActivity(), now = new Date()): number {
  const days = new Set(activity);
  let cursor = new Date(now);
  let key = cursor.toISOString().slice(0, 10);
  if (!days.has(key)) {
    cursor.setDate(cursor.getDate() - 1);
    key = cursor.toISOString().slice(0, 10);
    if (!days.has(key)) return 0;
  }
  let streak = 0;
  while (days.has(key)) {
    streak += 1;
    cursor.setDate(cursor.getDate() - 1);
    key = cursor.toISOString().slice(0, 10);
  }
  return streak;
}

export function toggleBookmark(slug: string): boolean {
  if (typeof window === "undefined") return false;
  const key = "ipbd.bookmarks.v1";
  let values: string[] = [];
  try {
    values = JSON.parse(window.localStorage.getItem(key) || "[]") as string[];
  } catch {
    values = [];
  }
  const next = new Set(values);
  if (next.has(slug)) next.delete(slug);
  else next.add(slug);
  window.localStorage.setItem(key, JSON.stringify([...next]));
  recordActivity();
  return next.has(slug);
}

export function readBookmarks(): string[] {
  if (typeof window === "undefined") return [];
  try {
    const values = JSON.parse(window.localStorage.getItem("ipbd.bookmarks.v1") || "[]");
    return Array.isArray(values) ? values.filter((item) => typeof item === "string") : [];
  } catch {
    return [];
  }
}
''',
"lib/utils.ts": r'''export function cx(...values: Array<string | false | null | undefined>): string {
  return values.filter(Boolean).join(" ");
}

export function difficultyTone(value: string): string {
  if (value === "Easy") return "border-emerald-400/20 bg-emerald-400/10 text-emerald-200";
  if (value === "Hard") return "border-rose-400/20 bg-rose-400/10 text-rose-200";
  return "border-amber-300/20 bg-amber-300/10 text-amber-100";
}

export function formatDate(value: string | null): string {
  if (!value) return "Not scheduled";
  return new Intl.DateTimeFormat("en-BD", { day: "numeric", month: "short", year: "numeric" }).format(new Date(value));
}
''',
"lib/supabase.ts": r'''import { createClient } from "@supabase/supabase-js";

export function getSupabaseAdmin() {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) return null;
  return createClient(url, key, { auth: { persistSession: false, autoRefreshToken: false } });
}''',
"app/globals.css": r'''@tailwind base;
@tailwind components;
@tailwind utilities;

:root { color-scheme: dark; }
html { scroll-behavior: smooth; background: #070a12; }
body { min-height: 100vh; background: radial-gradient(circle at 75% -12%, rgba(61, 109, 137, 0.18), transparent 34rem), #070a12; color: #e9eef8; }
::selection { background: rgba(117, 240, 193, 0.28); color: #fff; }
button, a, input, select, textarea { -webkit-tap-highlight-color: transparent; }
button:focus-visible, a:focus-visible, input:focus-visible, select:focus-visible, textarea:focus-visible { outline: 2px solid #75f0c1; outline-offset: 3px; }
.pretty-code pre, pre[data-theme], .prose pre { overflow-x: auto; border: 1px solid #202a3d; border-radius: 14px; padding: 1rem; background: #080d17 !important; font-size: 0.82rem; line-height: 1.7; }
pre code { background: transparent !important; }
.prose { color: #c8d2e3; max-width: none; }
.prose h2 { color: #f0f5ff; margin-top: 2.1rem; margin-bottom: 0.8rem; font-size: 1.3rem; font-weight: 700; letter-spacing: -0.025em; }
.prose h3 { color: #e8f1ff; margin-top: 1.5rem; font-size: 1.05rem; font-weight: 650; }
.prose p { margin: 0.8rem 0; line-height: 1.85; }
.prose ul { list-style: disc; padding-left: 1.3rem; margin: 0.9rem 0; }
.prose li { padding-left: 0.25rem; margin: 0.4rem 0; line-height: 1.75; }
.prose strong { color: #f2f6ff; font-weight: 650; }
.prose a { color: #90c9ff; text-decoration: underline; text-underline-offset: 3px; }
.prose blockquote { border-left: 2px solid #75f0c1; padding: 0.4rem 1rem; color: #d0dae9; background: rgba(117, 240, 193, 0.04); border-radius: 0 10px 10px 0; }
.prose code:not(pre code) { border: 1px solid #253149; background: #111a2a; padding: 0.12rem 0.34rem; border-radius: 5px; color: #a8d7ff; font-size: 0.9em; }
.panel { border: 1px solid rgba(148, 163, 184, 0.16); background: linear-gradient(145deg, rgba(17, 25, 41, 0.92), rgba(10, 15, 26, 0.94)); border-radius: 18px; }
.soft-grid { background-image: linear-gradient(rgba(148,163,184,.045) 1px, transparent 1px), linear-gradient(90deg, rgba(148,163,184,.045) 1px, transparent 1px); background-size: 30px 30px; }
''',
"app/layout.tsx": r'''import type { Metadata, Viewport } from "next";
import "./globals.css";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { SiteStructuredData } from "@/components/SiteStructuredData";
import { SITE_URL, DEFAULT_DESCRIPTION, KEYWORDS } from "@/lib/seo";

export const metadata: Metadata = {
  metadataBase: new URL("https://rafahim.com"),
  title: { default: "InterviewPrep BD by RA Fahim", template: "%s | InterviewPrep BD by RA Fahim" },
  description: DEFAULT_DESCRIPTION,
  keywords: KEYWORDS,
  authors: [{ name: "RA Fahim", url: "https://rafahim.com" }],
  creator: "RA Fahim",
  alternates: { canonical: `${SITE_URL}/` },
  openGraph: {
    type: "website",
    locale: "en_BD",
    url: `${SITE_URL}/`,
    siteName: "InterviewPrep BD",
    title: "InterviewPrep BD by RA Fahim",
    description: DEFAULT_DESCRIPTION,
    images: [{ url: `${SITE_URL}/og-image.svg`, width: 1200, height: 630, alt: "InterviewPrep BD by RA Fahim" }]
  },
  twitter: {
    card: "summary_large_image",
    creator: "@rafahimn",
    title: "InterviewPrep BD by RA Fahim",
    description: DEFAULT_DESCRIPTION,
    images: [`${SITE_URL}/og-image.svg`]
  },
  manifest: "/interview-prep/manifest.json",
  icons: { icon: "/interview-prep/favicon.svg", shortcut: "/interview-prep/favicon.svg" }
};

export const viewport: Viewport = {
  themeColor: "#070a12",
  colorScheme: "dark",
  width: "device-width",
  initialScale: 1
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="bn" className="dark">
      <body className="font-sans antialiased">
        <SiteStructuredData />
        <Navbar />
        <main className="min-h-[calc(100vh-160px)]">{children}</main>
        <Footer />
      </body>
    </html>
  );
}''',
"components/SiteStructuredData.tsx": r'''import { SITE_URL, DEFAULT_DESCRIPTION } from "@/lib/seo";

export function SiteStructuredData() {
  const schema = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Person",
        "name": "RA Fahim",
        "url": "https://rafahim.com",
        "jobTitle": "Web Developer & Creator",
        "description": "Full-stack web developer with 1 year of experience, based in Dhaka, Bangladesh.",
        "address": { "@type": "PostalAddress", "addressLocality": "Dhaka", "addressCountry": "BD" },
        "sameAs": ["https://github.com/rafahim", "https://twitter.com/rafahimn", "https://linkedin.com/in/rafahimn"]
      },
      {
        "@type": "WebSite",
        "name": "InterviewPrep BD",
        "url": `${SITE_URL}/`,
        "description": DEFAULT_DESCRIPTION,
        "inLanguage": ["bn", "en"],
        "publisher": { "@type": "Person", "name": "RA Fahim", "url": "https://rafahim.com" }
      }
    ]
  };
  return <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />;
}''',
"components/Footer.tsx": r'''import Link from "next/link";

export function Footer() {
  return (
    <footer className="border-t border-white/5 mt-20">
      <div className="mx-auto flex max-w-7xl flex-col gap-3 px-5 py-7 text-sm text-slate-500 sm:flex-row sm:items-center sm:justify-between sm:px-8">
        <p>Built with ❤️ by <a className="text-slate-300 hover:text-mint" href="https://rafahim.com">RA Fahim</a> · <a className="text-slate-300 hover:text-mint" href="https://rafahim.com">rafahim.com</a> · © 2026 RA Fahim</p>
        <div className="flex flex-wrap gap-4">
          <Link className="hover:text-slate-200" href="/questions/">Questions</Link>
          <Link className="hover:text-slate-200" href="/practice/">Practice</Link>
          <a className="hover:text-slate-200" href="https://github.com/rafahim/interviewprep-bd">Contribute on GitHub</a>
        </div>
      </div>
    </footer>
  );
}''',
"components/LanguageToggle.tsx": r'''export function LanguageToggle() {
  return <span className="rounded-full border border-white/10 px-3 py-1.5 text-xs font-semibold text-slate-300">বাংলা · EN</span>;
}''', 
"components/Navbar.tsx": r'''import Link from "next/link";
import { Search } from "@/components/Search";
import { LanguageToggle } from "@/components/LanguageToggle";

const links = [
  { href: "/questions/", label: "Questions" },
  { href: "/practice/", label: "Practice" },
  { href: "/flashcards/", label: "Flashcards" },
  { href: "/progress/", label: "Progress" }
];

export function Navbar() {
  return (
    <header className="sticky top-0 z-40 border-b border-white/[0.07] bg-ink/85 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-5 py-3.5 sm:px-8">
        <Link href="/" className="group flex min-w-0 items-center gap-2.5">
          <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-mint text-sm font-black text-ink shadow-glow">IP</span>
          <span className="min-w-0"><span className="block truncate text-sm font-bold tracking-tight text-white sm:text-base">InterviewPrep <span className="text-mint">BD</span></span><span className="hidden text-[10px] tracking-[0.16em] text-slate-500 sm:block">BY RA FAHIM</span></span>
        </Link>
        <nav className="hidden items-center gap-5 lg:flex">
          {links.map((link) => <Link key={link.href} href={link.href} className="text-sm text-slate-400 transition hover:text-white">{link.label}</Link>)}
        </nav>
        <div className="flex shrink-0 items-center gap-2.5"><Search /><LanguageToggle /></div>
      </div>
      <nav className="mx-auto flex max-w-7xl gap-5 overflow-x-auto px-5 pb-3 text-xs text-slate-400 sm:px-8 lg:hidden">
        {links.map((link) => <Link key={link.href} href={link.href} className="whitespace-nowrap transition hover:text-mint">{link.label}</Link>)}
      </nav>
    </header>
  );
}''',
"components/Search.tsx": r'''"use client";

import Fuse from "fuse.js";
import Link from "next/link";
import { useCallback, useEffect, useMemo, useState } from "react";
import type { QuestionIndexItem } from "@/types";

export function Search() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [questions, setQuestions] = useState<QuestionIndexItem[]>([]);
  const [loading, setLoading] = useState(false);
  const openSearch = useCallback(() => setOpen(true), []);

  useEffect(() => {
    function onKeyDown(event: KeyboardEvent) {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        openSearch();
      }
      if (event.key === "Escape") setOpen(false);
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [openSearch]);

  useEffect(() => {
    if (!open || questions.length) return;
    setLoading(true);
    fetch("/interview-prep/api/questions/")
      .then((response) => response.ok ? response.json() : [])
      .then((data: QuestionIndexItem[]) => setQuestions(Array.isArray(data) ? data : []))
      .catch(() => setQuestions([]))
      .finally(() => setLoading(false));
  }, [open, questions.length]);

  const fuse = useMemo(() => new Fuse(questions, {
    keys: ["title", "topic", "problem", "tags", "companies", "category"],
    threshold: 0.36,
    ignoreLocation: true
  }), [questions]);
  const results = useMemo(() => {
    if (!query.trim()) return questions.slice(0, 6);
    return fuse.search(query.trim(), { limit: 8 }).map((item) => item.item);
  }, [fuse, query, questions]);

  return <>
    <button onClick={openSearch} className="flex items-center gap-2 rounded-xl border border-white/10 bg-white/[0.035] px-3 py-2 text-xs text-slate-400 transition hover:border-mint/40 hover:text-white" aria-label="Search questions">
      <span aria-hidden="true">⌕</span><span className="hidden sm:inline">Search</span><kbd className="hidden rounded border border-white/10 px-1.5 py-0.5 font-mono text-[10px] sm:inline">⌘K</kbd>
    </button>
    {open && <div className="fixed inset-0 z-[70] flex items-start justify-center bg-black/70 px-4 pt-[12vh] backdrop-blur-sm" onMouseDown={(event) => { if (event.target === event.currentTarget) setOpen(false); }}>
      <section className="w-full max-w-2xl overflow-hidden rounded-2xl border border-white/10 bg-[#0c1220] shadow-2xl" role="dialog" aria-modal="true" aria-label="Search interview questions">
        <div className="flex items-center gap-3 border-b border-white/10 px-4">
          <span className="text-xl text-mint">⌕</span>
          <input autoFocus value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search questions, topics, companies…" className="w-full bg-transparent py-4 text-sm text-white outline-none placeholder:text-slate-500" />
          <button onClick={() => setOpen(false)} className="rounded-md border border-white/10 px-2 py-1 text-[10px] text-slate-400">ESC</button>
        </div>
        <div className="max-h-[52vh] overflow-y-auto p-2">
          {loading && <p className="px-3 py-6 text-sm text-slate-500">Loading question index…</p>}
          {!loading && results.length === 0 && <p className="px-3 py-6 text-sm text-slate-500">No matching question. অন্য keyword দিয়ে চেষ্টা করো।</p>}
          {results.map((item) => <Link key={item.slug} onClick={() => setOpen(false)} href={`/questions/${item.slug}/`} className="flex items-center justify-between gap-3 rounded-xl px-3 py-3 transition hover:bg-white/[0.06]">
            <span className="min-w-0"><span className="block truncate text-sm font-semibold text-slate-100">{item.title}</span><span className="mt-1 block truncate text-xs text-slate-500">{item.topic} · {item.difficulty}</span></span>
            <span className="shrink-0 text-slate-600">↗</span>
          </Link>)}
        </div>
        <div className="flex items-center justify-between border-t border-white/10 px-4 py-2.5 text-[10px] text-slate-600"><span>বাংলা + English · {questions.length || "…"} questions</span><span>ESC to close</span></div>
      </section>
    </div>}
  </>;
}''',
"components/QuestionCard.tsx": r'''import Link from "next/link";
import type { QuestionIndexItem } from "@/types";
import { CATEGORY_LABELS } from "@/lib/categories";
import { difficultyTone } from "@/lib/utils";

export function QuestionCard({ question, index }: { question: QuestionIndexItem; index?: number }) {
  return <article className="group panel flex h-full flex-col p-5 transition duration-200 hover:-translate-y-0.5 hover:border-mint/30 hover:shadow-glow">
    <div className="flex items-center justify-between gap-3"><span className="text-[11px] font-semibold uppercase tracking-[0.14em] text-slate-500">{CATEGORY_LABELS[question.category]}</span><span className={`rounded-full border px-2.5 py-1 text-[10px] font-semibold ${difficultyTone(question.difficulty)}`}>{question.difficulty}</span></div>
    <Link href={`/questions/${question.slug}/`} className="mt-4 block"><h3 className="text-base font-semibold leading-snug text-slate-100 transition group-hover:text-mint">{index ? <span className="mr-2 font-mono text-xs text-slate-600">{String(index).padStart(2, "0")}</span> : null}{question.title}</h3></Link>
    <p className="mt-2 line-clamp-3 flex-1 text-sm leading-6 text-slate-400">{question.problem}</p>
    <div className="mt-4 flex flex-wrap gap-1.5">{question.tags.slice(0, 3).map((tag) => <span key={tag} className="rounded-md border border-white/[0.07] bg-white/[0.025] px-2 py-1 text-[10px] text-slate-500">{tag}</span>)}</div>
    <div className="mt-5 flex items-center justify-between border-t border-white/[0.07] pt-4 text-xs text-slate-500"><span>{question.minutes} min · {question.frequency} frequency</span><Link href={`/questions/${question.slug}/`} className="font-semibold text-slate-300 transition group-hover:text-mint">Study ↗</Link></div>
  </article>;
}''',
"components/FilterBar.tsx": r'''"use client";

import type { QuestionCategory } from "@/types";

export type BrowserFilters = { category: string; difficulty: string; topic: string; company: string; language: string; frequency: string; sort: string };
type Props = { filters: BrowserFilters; onChange: (filters: BrowserFilters) => void; categories: { id: QuestionCategory; label: string }[]; topics: string[]; companies: string[]; languages: string[] };

const selectClass = "min-w-0 rounded-xl border border-white/10 bg-[#0c1220] px-3 py-2.5 text-xs text-slate-300 outline-none transition focus:border-mint/40";

export function FilterBar({ filters, onChange, categories, topics, companies, languages }: Props) {
  function change(key: keyof BrowserFilters, value: string) { onChange({ ...filters, [key]: value }); }
  return <div className="panel p-3 sm:p-4">
    <div className="grid grid-cols-2 gap-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-7">
      <select aria-label="Category" className={selectClass} value={filters.category} onChange={(event) => change("category", event.target.value)}><option value="">All categories</option>{categories.map((item) => <option key={item.id} value={item.id}>{item.label}</option>)}</select>
      <select aria-label="Difficulty" className={selectClass} value={filters.difficulty} onChange={(event) => change("difficulty", event.target.value)}><option value="">All difficulty</option><option>Easy</option><option>Medium</option><option>Hard</option></select>
      <select aria-label="Topic" className={selectClass} value={filters.topic} onChange={(event) => change("topic", event.target.value)}><option value="">All topics</option>{topics.map((value) => <option key={value}>{value}</option>)}</select>
      <select aria-label="Company" className={selectClass} value={filters.company} onChange={(event) => change("company", event.target.value)}><option value="">All companies</option>{companies.map((value) => <option key={value}>{value}</option>)}</select>
      <select aria-label="Language" className={selectClass} value={filters.language} onChange={(event) => change("language", event.target.value)}><option value="">All languages</option>{languages.map((value) => <option key={value}>{value}</option>)}</select>
      <select aria-label="Frequency" className={selectClass} value={filters.frequency} onChange={(event) => change("frequency", event.target.value)}><option value="">All frequency</option><option>High</option><option>Medium</option><option>Low</option></select>
      <select aria-label="Sort questions" className={selectClass} value={filters.sort} onChange={(event) => change("sort", event.target.value)}><option value="recommended">Recommended</option><option value="title">Title A–Z</option><option value="difficulty">Difficulty</option><option value="time">Time needed</option><option value="frequency">Frequency</option></select>
    </div>
    <div className="mt-3 flex justify-end"><button onClick={() => onChange({ category: "", difficulty: "", topic: "", company: "", language: "", frequency: "", sort: "recommended" })} className="text-xs text-slate-500 transition hover:text-mint">Reset filters ↺</button></div>
  </div>;
}''',
"components/QuestionBrowser.tsx": r'''"use client";

import Fuse from "fuse.js";
import { useMemo, useState } from "react";
import type { QuestionCategory, QuestionIndexItem } from "@/types";
import { CATEGORY_LABELS, CATEGORY_ORDER } from "@/lib/categories";
import { FilterBar, type BrowserFilters } from "@/components/FilterBar";
import { QuestionCard } from "@/components/QuestionCard";

const initialFilters: BrowserFilters = { category: "", difficulty: "", topic: "", company: "", language: "", frequency: "", sort: "recommended" };
const difficultyOrder: Record<string, number> = { Easy: 1, Medium: 2, Hard: 3 };

export function QuestionBrowser({ questions, initialCategory = "" }: { questions: QuestionIndexItem[]; initialCategory?: string }) {
  const [query, setQuery] = useState("");
  const [filters, setFilters] = useState<BrowserFilters>({ ...initialFilters, category: initialCategory });
  const fuse = useMemo(() => new Fuse(questions, { keys: ["title", "problem", "topic", "tags", "companies", "category"], threshold: 0.38, ignoreLocation: true }), [questions]);
  const topics = useMemo(() => [...new Set(questions.map((question) => question.topic))].sort(), [questions]);
  const companies = useMemo(() => [...new Set(questions.flatMap((question) => question.companies))].sort(), [questions]);
  const languages = useMemo(() => [...new Set(questions.flatMap((question) => question.languages))].sort(), [questions]);
  const filtered = useMemo(() => {
    const source = query.trim() ? fuse.search(query.trim()).map((result) => result.item) : questions;
    const result = source.filter((question) => (!filters.category || question.category === filters.category) && (!filters.difficulty || question.difficulty === filters.difficulty) && (!filters.topic || question.topic === filters.topic) && (!filters.company || question.companies.includes(filters.company)) && (!filters.language || question.languages.includes(filters.language)) && (!filters.frequency || question.frequency === filters.frequency));
    if (filters.sort === "title") result.sort((a, b) => a.title.localeCompare(b.title));
    if (filters.sort === "difficulty") result.sort((a, b) => difficultyOrder[a.difficulty] - difficultyOrder[b.difficulty] || a.title.localeCompare(b.title));
    if (filters.sort === "time") result.sort((a, b) => a.minutes - b.minutes);
    if (filters.sort === "frequency") result.sort((a, b) => ["High", "Medium", "Low"].indexOf(a.frequency) - ["High", "Medium", "Low"].indexOf(b.frequency));
    return result;
  }, [filters, fuse, questions, query]);
  const categories = CATEGORY_ORDER.map((id: QuestionCategory) => ({ id, label: CATEGORY_LABELS[id] }));
  return <div className="space-y-5">
    <div className="flex flex-col gap-3 sm:flex-row"><label className="relative flex-1"><span className="sr-only">Search questions</span><span className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-slate-500">⌕</span><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search by question, concept, company…" className="w-full rounded-xl border border-white/10 bg-white/[0.035] py-3 pl-11 pr-4 text-sm text-white outline-none placeholder:text-slate-600 focus:border-mint/40" /></label><div className="flex items-center justify-between rounded-xl border border-white/10 px-4 py-3 text-xs text-slate-400 sm:min-w-40"><span>Matching questions</span><strong className="text-mint">{filtered.length} / {questions.length}</strong></div></div>
    <FilterBar filters={filters} onChange={setFilters} categories={categories} topics={topics} companies={companies} languages={languages} />
    {filtered.length ? <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">{filtered.map((question, index) => <QuestionCard key={question.slug} question={question} index={index + 1} />)}</div> : <div className="panel px-6 py-16 text-center"><p className="text-lg font-semibold text-slate-200">No questions found</p><p className="mt-2 text-sm text-slate-500">Search term বা filter পরিবর্তন করে আবার চেষ্টা করো।</p><button onClick={() => { setQuery(""); setFilters(initialFilters); }} className="mt-5 rounded-xl bg-mint px-4 py-2.5 text-sm font-bold text-ink">Clear filters</button></div>}
  </div>;
}''',
"components/CodeBlock.tsx": r'''import { codeToHtml } from "shiki";

export async function CodeBlock({ code, language = "text", title }: { code: string; language?: string; title?: string }) {
  const html = await codeToHtml(code, { lang: language, theme: "github-dark" });
  return <div className="my-4 overflow-hidden rounded-2xl border border-line bg-[#080d17]">{title && <div className="border-b border-line px-4 py-2 text-xs text-slate-500">{title}</div>}<div className="pretty-code" dangerouslySetInnerHTML={{ __html: html }} /></div>;
}''',
"components/Timer.tsx": r'''"use client";

import { useEffect, useState } from "react";

function clock(seconds: number) {
  const minutes = Math.floor(seconds / 60).toString().padStart(2, "0");
  const remaining = (seconds % 60).toString().padStart(2, "0");
  return `${minutes}:${remaining}`;
}

export function Timer({ initialMinutes = 30 }: { initialMinutes?: number }) {
  const [duration, setDuration] = useState(initialMinutes * 60);
  const [remaining, setRemaining] = useState(initialMinutes * 60);
  const [running, setRunning] = useState(false);
  useEffect(() => {
    if (!running || remaining <= 0) return;
    const id = window.setInterval(() => setRemaining((value) => Math.max(0, value - 1)), 1000);
    return () => window.clearInterval(id);
  }, [running, remaining]);
  useEffect(() => { if (remaining === 0) setRunning(false); }, [remaining]);
  function reset() { setRunning(false); setRemaining(duration); }
  return <div className="panel flex flex-wrap items-center justify-between gap-4 p-4">
    <div><p className="text-[10px] font-bold uppercase tracking-[0.16em] text-slate-500">Mock interview timer</p><p className={`mt-1 font-mono text-3xl font-bold tabular-nums ${remaining <= 60 ? "text-rose-300" : "text-white"}`}>{clock(remaining)}</p></div>
    <div className="flex flex-wrap items-center gap-2"><select aria-label="Timer duration" value={duration / 60} onChange={(event) => { const next = Number(event.target.value) * 60; setDuration(next); setRemaining(next); setRunning(false); }} className="rounded-lg border border-white/10 bg-[#0c1220] px-2.5 py-2 text-xs text-slate-300"><option value="15">15 min</option><option value="30">30 min</option><option value="45">45 min</option><option value="60">60 min</option></select><button onClick={() => remaining > 0 && setRunning((value) => !value)} className="rounded-lg bg-mint px-3 py-2 text-xs font-bold text-ink">{running ? "Pause" : "Start"}</button><button onClick={reset} className="rounded-lg border border-white/10 px-3 py-2 text-xs text-slate-300">Reset</button></div>
  </div>;
}''',
"components/ProgressChart.tsx": r'''type Segment = { label: string; value: number; color: string };

export function ProgressChart({ data, total }: { data: Segment[]; total: number }) {
  return <div className="panel p-5"><div className="flex items-center justify-between"><h3 className="font-semibold text-slate-100">Progress overview</h3><span className="text-xs text-slate-500">{total} questions</span></div><div className="mt-5 space-y-4">{data.map((item) => <div key={item.label}><div className="mb-2 flex items-center justify-between text-xs"><span className="text-slate-400">{item.label}</span><span className="font-mono text-slate-300">{item.value} <span className="text-slate-600">/ {total}</span></span></div><div className="h-2 overflow-hidden rounded-full bg-white/[0.05]"><div className={`h-full rounded-full ${item.color}`} style={{ width: `${total ? Math.min(100, (item.value / total) * 100) : 0}%` }} /></div></div>)}</div></div>;
}''',
"components/QuestionActions.tsx": r'''"use client";

import { useEffect, useState } from "react";
import type { ProgressStatus } from "@/types";
import { readBookmarks, readProgress, saveStatus, toggleBookmark } from "@/lib/progress";

export function QuestionActions({ slug, title, content }: { slug: string; title: string; content: string }) {
  const [bookmarked, setBookmarked] = useState(false);
  const [status, setStatus] = useState<ProgressStatus>("todo");
  const [message, setMessage] = useState("");
  useEffect(() => {
    setBookmarked(readBookmarks().includes(slug));
    setStatus(readProgress()[slug]?.status || "todo");
  }, [slug]);
  async function share() {
    const url = window.location.href;
    try {
      if (navigator.share) await navigator.share({ title, url });
      else { await navigator.clipboard.writeText(url); setMessage("Link copied to clipboard."); }
    } catch { setMessage("Share was cancelled or unavailable."); }
  }
  async function copy() {
    try { await navigator.clipboard.writeText(`${title}\n\n${content}`); setMessage("Question and explanation copied."); }
    catch { setMessage("Clipboard access is unavailable in this browser."); }
  }
  async function feedback(rating: "helpful" | "needs-work") {
    try {
      const response = await fetch("/interview-prep/api/feedback/", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ slug, rating }) });
      const data = await response.json();
      setMessage(data.persisted ? "Thanks — feedback saved." : "Thanks — feedback received for this session; configure Supabase to store it.");
    } catch { setMessage("Feedback could not be sent. Please try again."); }
  }
  function updateStatus(next: ProgressStatus) { saveStatus(slug, next); setStatus(next); setMessage(`Status updated: ${next.replace("-", " ")}.`); }
  return <div className="panel space-y-4 p-4">
    <div><p className="text-[10px] font-bold uppercase tracking-[0.16em] text-slate-500">Your workspace</p><select aria-label="Question progress status" value={status} onChange={(event) => updateStatus(event.target.value as ProgressStatus)} className="mt-2 w-full rounded-xl border border-white/10 bg-[#0b101c] px-3 py-2.5 text-xs text-slate-200"><option value="todo">To do</option><option value="in-progress">In progress</option><option value="solved">Solved</option><option value="needs-review">Needs review</option></select></div>
    <div className="grid grid-cols-2 gap-2"><button onClick={() => { setBookmarked(toggleBookmark(slug)); setMessage(bookmarked ? "Removed from bookmarks." : "Saved to bookmarks."); }} className="rounded-xl border border-white/10 px-3 py-2.5 text-xs font-semibold text-slate-300 transition hover:border-mint/40 hover:text-mint">{bookmarked ? "★ Bookmarked" : "☆ Bookmark"}</button><button onClick={share} className="rounded-xl border border-white/10 px-3 py-2.5 text-xs font-semibold text-slate-300 transition hover:border-mint/40 hover:text-mint">Share ↗</button></div>
    <button onClick={copy} className="w-full rounded-xl border border-white/10 px-3 py-2.5 text-xs font-semibold text-slate-300 transition hover:border-mint/40 hover:text-mint">Copy question + explanation</button>
    <div className="border-t border-white/[0.07] pt-3"><p className="text-xs font-semibold text-slate-300">Was this explanation helpful?</p><div className="mt-2 grid grid-cols-2 gap-2"><button onClick={() => feedback("helpful")} className="rounded-lg bg-white/[0.04] px-2 py-2 text-xs text-slate-400 hover:text-mint">Yes, helpful</button><button onClick={() => feedback("needs-work")} className="rounded-lg bg-white/[0.04] px-2 py-2 text-xs text-slate-400 hover:text-amber">Needs work</button></div></div>
    {message && <p role="status" className="text-xs leading-5 text-mint">{message}</p>}
  </div>;
}'''
}

FILES.update({
"components/PracticeRoom.tsx": r'''"use client";

import { useMemo, useState } from "react";
import type { QuestionIndexItem } from "@/types";
import { QuestionCard } from "@/components/QuestionCard";
import { Timer } from "@/components/Timer";
import { recordActivity, reviewQuestion } from "@/lib/progress";

export function PracticeRoom({ questions }: { questions: QuestionIndexItem[] }) {
  const [category, setCategory] = useState("all");
  const [difficulty, setDifficulty] = useState("all");
  const [current, setCurrent] = useState<QuestionIndexItem | null>(null);
  const [notes, setNotes] = useState("");
  const [savedNotes, setSavedNotes] = useState("");
  const [rating, setRating] = useState(3);
  const [mode, setMode] = useState("random");
  const [session, setSession] = useState<QuestionIndexItem[]>([]);
  const pool = useMemo(() => questions.filter((question) => (category === "all" || question.category === category) && (difficulty === "all" || question.difficulty === difficulty)), [category, difficulty, questions]);

  function chooseQuestion() {
    if (!pool.length) return;
    const item = pool[Math.floor(Math.random() * pool.length)];
    setCurrent(item);
    setNotes("");
    setSavedNotes("");
    setSession((previous) => [...previous.filter((entry) => entry.slug !== item.slug), item].slice(-10));
    recordActivity();
  }

  function startMock() {
    const shuffled = [...pool].sort(() => Math.random() - 0.5).slice(0, Math.min(5, pool.length));
    setSession(shuffled);
    setCurrent(shuffled[0] || null);
    setMode("mock");
    setNotes("");
    setSavedNotes("");
    recordActivity();
  }

  function saveNote() {
    if (!current) return;
    const key = `ipbd.notes.${current.slug}`;
    window.localStorage.setItem(key, notes);
    setSavedNotes("Notes saved on this device.");
    recordActivity();
  }

  function rate(value: number) {
    if (!current) return;
    setRating(value);
    reviewQuestion(current.slug, value);
    setSavedNotes("Self-rating saved. Spaced repetition date updated.");
  }

  return <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_320px]">
    <section className="space-y-5">
      <div className="panel p-5 sm:p-6"><div className="flex flex-wrap items-center justify-between gap-3"><div><p className="text-[10px] font-bold uppercase tracking-[0.18em] text-mint">Practice workspace</p><h2 className="mt-2 text-xl font-semibold text-white">Pick a question and think out loud</h2><p className="mt-2 text-sm leading-6 text-slate-400">প্রথমে problem restate করো, assumptions জিজ্ঞেস করো, তারপর approach ও complexity বোঝাও।</p></div><span className="rounded-full border border-mint/20 bg-mint/10 px-3 py-1.5 text-xs text-mint">Local-only notes</span></div>
        <div className="mt-5 grid gap-3 sm:grid-cols-2"><label className="text-xs text-slate-500">Topic<select value={category} onChange={(event) => setCategory(event.target.value)} className="mt-2 w-full rounded-xl border border-white/10 bg-[#0b101c] px-3 py-3 text-sm text-slate-200"><option value="all">All topics</option><option value="dsa">DSA</option><option value="system-design">System Design</option><option value="database">Database</option><option value="behavioral">Behavioral</option><option value="languages">Languages</option><option value="bangladesh">Bangladesh interviews</option></select></label><label className="text-xs text-slate-500">Difficulty<select value={difficulty} onChange={(event) => setDifficulty(event.target.value)} className="mt-2 w-full rounded-xl border border-white/10 bg-[#0b101c] px-3 py-3 text-sm text-slate-200"><option value="all">All levels</option><option>Easy</option><option>Medium</option><option>Hard</option></select></label></div>
        <div className="mt-4 flex flex-wrap gap-2"><button onClick={chooseQuestion} disabled={!pool.length} className="rounded-xl bg-mint px-4 py-3 text-sm font-bold text-ink transition hover:bg-white disabled:opacity-40">Pick random question ↗</button><button onClick={startMock} disabled={!pool.length} className="rounded-xl border border-white/10 px-4 py-3 text-sm font-semibold text-slate-300 transition hover:border-mint/30 hover:text-mint disabled:opacity-40">Start 5-question mock</button></div>
      </div>
      {current ? <div className="panel p-5 sm:p-6"><div className="flex flex-wrap items-center justify-between gap-3"><span className="text-xs uppercase tracking-[0.14em] text-slate-500">{mode === "mock" ? `Mock interview · ${session.findIndex((item) => item.slug === current.slug) + 1}/${session.length}` : "Selected question"}</span><span className="text-xs text-slate-500">{current.minutes} minute target</span></div><h3 className="mt-3 text-2xl font-bold tracking-tight text-white">{current.title}</h3><p className="mt-3 leading-7 text-slate-300">{current.problem}</p><div className="mt-4 flex flex-wrap gap-2">{current.tags.map((tag) => <span key={tag} className="rounded-lg border border-white/10 px-2.5 py-1.5 text-[11px] text-slate-500">{tag}</span>)}</div><div className="mt-6"><label className="text-xs font-semibold text-slate-300">Your approach / interview notes<textarea value={notes} onChange={(event) => setNotes(event.target.value)} rows={6} placeholder="Write assumptions, brute force, optimized approach, complexity and edge cases…" className="mt-2 w-full resize-y rounded-xl border border-white/10 bg-[#080d17] p-3 text-sm leading-6 text-slate-200 outline-none placeholder:text-slate-600 focus:border-mint/30" /></label><div className="mt-3 flex flex-wrap items-center justify-between gap-3"><button onClick={saveNote} className="rounded-lg border border-white/10 px-3 py-2 text-xs font-semibold text-slate-300 hover:border-mint/30 hover:text-mint">Save notes on device</button>{savedNotes && <span role="status" className="text-xs text-mint">{savedNotes}</span>}</div></div><div className="mt-6 border-t border-white/[0.07] pt-5"><p className="text-xs font-semibold text-slate-300">Self-rate this attempt</p><div className="mt-3 flex flex-wrap gap-2">{[{ value: 1, label: "Again" }, { value: 3, label: "Good" }, { value: 5, label: "Easy" }].map((option) => <button key={option.value} onClick={() => rate(option.value)} className={`rounded-lg border px-4 py-2.5 text-xs font-semibold ${rating === option.value ? "border-mint/40 bg-mint/10 text-mint" : "border-white/10 text-slate-400 hover:text-white"}`}>{option.label}</button>)}</div></div><div className="mt-6"><a href={`/interview-prep/questions/${current.slug}/`} className="text-sm font-semibold text-sky hover:text-mint">Open full solution and explanation ↗</a></div>{mode === "mock" && <div className="mt-5 flex justify-between gap-3 border-t border-white/[0.07] pt-4"><button onClick={() => { const index = session.findIndex((item) => item.slug === current.slug); const next = session[Math.max(0, index - 1)]; if (next) setCurrent(next); }} className="rounded-lg border border-white/10 px-3 py-2 text-xs text-slate-400">Previous</button><button onClick={() => { const index = session.findIndex((item) => item.slug === current.slug); const next = session[index + 1]; if (next) { setCurrent(next); setNotes(""); setSavedNotes(""); } }} className="rounded-lg bg-mint px-3 py-2 text-xs font-bold text-ink">Next question →</button></div>}</div> : <div className="panel flex min-h-60 flex-col items-center justify-center p-8 text-center"><span className="text-3xl text-mint">◉</span><h3 className="mt-4 text-lg font-semibold text-slate-100">Your practice session starts here</h3><p className="mt-2 max-w-sm text-sm leading-6 text-slate-500">একটি random prompt নাও, আগে নিজে solve করো, তারপর full explanation খুলে নিজের উত্তর যাচাই করো।</p></div>}
      {session.length > 0 && <div><h3 className="mb-3 text-sm font-semibold text-slate-300">Recent session picks</h3><div className="grid gap-3 sm:grid-cols-2">{session.map((item) => <QuestionCard key={item.slug} question={item} />)}</div></div>}
    </section>
    <aside className="space-y-4"><Timer initialMinutes={30} /><div className="panel p-5"><p className="text-xs font-bold uppercase tracking-[0.15em] text-slate-500">Interview loop</p><div className="mt-4 space-y-4">{[{n:"01",t:"Clarify",d:"Input, constraints, examples"},{n:"02",t:"Plan",d:"Brute force → optimized approach"},{n:"03",t:"Implement",d:"Readable code and invariants"},{n:"04",t:"Verify",d:"Run examples and edge cases"},{n:"05",t:"Reflect",d:"Complexity and trade-offs"}].map((step) => <div key={step.n} className="flex gap-3"><span className="font-mono text-xs text-mint">{step.n}</span><div><p className="text-sm font-semibold text-slate-200">{step.t}</p><p className="mt-1 text-xs leading-5 text-slate-500">{step.d}</p></div></div>)}</div></div><div className="rounded-2xl border border-sky/15 bg-sky/[0.04] p-5"><p className="text-sm font-semibold text-sky">বাংলা + English practice</p><p className="mt-2 text-xs leading-6 text-slate-400">নিজের reasoning বাংলায় পরিষ্কার করো; interview-এর প্রয়োজন অনুযায়ী core technical terms ইংরেজিতে concise করে বলার অভ্যাস করো।</p></div></aside>
  </div>;
}''',
"components/Flashcards.tsx": r'''"use client";

import { useMemo, useState } from "react";
import type { QuestionIndexItem } from "@/types";
import { readProgress, reviewQuestion } from "@/lib/progress";

export function Flashcards({ questions }: { questions: QuestionIndexItem[] }) {
  const [index, setIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [filter, setFilter] = useState("due");
  const [revision, setRevision] = useState(0);
  const cards = useMemo(() => {
    const progress = readProgress();
    const now = Date.now();
    const sorted = [...questions].sort((a, b) => a.title.localeCompare(b.title));
    if (filter === "all") return sorted;
    if (filter === "bookmarked") {
      let bookmarks: string[] = [];
      try { bookmarks = JSON.parse(window.localStorage.getItem("ipbd.bookmarks.v1") || "[]") as string[]; } catch { bookmarks = []; }
      return sorted.filter((question) => bookmarks.includes(question.slug));
    }
    return sorted.filter((question) => {
      const item = progress[question.slug];
      if (!item || !item.nextReview) return true;
      return new Date(item.nextReview).getTime() <= now;
    });
  }, [filter, questions, revision]);
  const current = cards.length ? cards[index % cards.length] : null;

  function move(direction: number) {
    setIndex((value) => cards.length ? (value + direction + cards.length) % cards.length : 0);
    setFlipped(false);
  }

  function rate(value: number) {
    if (!current) return;
    reviewQuestion(current.slug, value);
    setRevision((previous) => previous + 1);
    setFlipped(false);
    setIndex((previous) => cards.length ? (previous + 1) % cards.length : 0);
  }

  return <div className="mx-auto max-w-4xl space-y-6">
    <div className="flex flex-wrap items-end justify-between gap-4"><div><p className="text-xs font-bold uppercase tracking-[0.18em] text-mint">Recall practice</p><h2 className="mt-2 text-3xl font-bold tracking-tight text-white">Flashcards</h2><p className="mt-2 text-sm text-slate-400">প্রশ্ন থেকে card স্বয়ংক্রিয়ভাবে তৈরি হয়েছে। আগে উত্তর মনে করার চেষ্টা করো, তারপর reveal করো।</p></div><label className="text-xs text-slate-500">Card set<select value={filter} onChange={(event) => { setFilter(event.target.value); setIndex(0); setFlipped(false); }} className="mt-2 block rounded-xl border border-white/10 bg-[#0c1220] px-3 py-2.5 text-sm text-slate-200"><option value="due">Due for review</option><option value="all">All flashcards</option><option value="bookmarked">Bookmarked</option></select></label></div>
    {current ? <><div className="flex items-center justify-between text-xs text-slate-500"><span>Card {index + 1} of {cards.length}</span><span>{current.topic} · {current.difficulty}</span></div><button onClick={() => setFlipped((value) => !value)} className="soft-grid panel flex min-h-[340px] w-full flex-col items-center justify-center p-8 text-center transition hover:border-mint/30 sm:min-h-[390px]" aria-label="Flip flashcard"><span className="rounded-full border border-mint/20 bg-mint/10 px-3 py-1 text-[10px] font-bold uppercase tracking-[0.16em] text-mint">{flipped ? "Answer" : "Recall"}</span><span className="mt-8 max-w-2xl text-2xl font-semibold leading-relaxed text-white sm:text-3xl">{flipped ? current.back : current.front}</span><span className="mt-8 text-xs text-slate-600">{flipped ? "Click to see the prompt" : "Click to reveal answer"}</span></button><div className="flex flex-wrap justify-center gap-2"><button onClick={() => move(-1)} className="rounded-xl border border-white/10 px-4 py-3 text-sm text-slate-300">← Previous</button><button onClick={() => setFlipped((value) => !value)} className="rounded-xl bg-mint px-5 py-3 text-sm font-bold text-ink">{flipped ? "Show prompt" : "Reveal answer"}</button><button onClick={() => move(1)} className="rounded-xl border border-white/10 px-4 py-3 text-sm text-slate-300">Next →</button></div>{flipped && <div className="panel p-5"><p className="text-center text-sm font-semibold text-slate-200">How well did you recall it?</p><div className="mt-4 grid grid-cols-3 gap-2"><button onClick={() => rate(1)} className="rounded-xl border border-rose-400/20 bg-rose-400/[0.05] px-3 py-3 text-xs font-semibold text-rose-200">Again · 1 day</button><button onClick={() => rate(3)} className="rounded-xl border border-amber/20 bg-amber/[0.05] px-3 py-3 text-xs font-semibold text-amber-100">Good · spaced</button><button onClick={() => rate(5)} className="rounded-xl border border-mint/20 bg-mint/[0.05] px-3 py-3 text-xs font-semibold text-mint">Easy · spaced</button></div><p className="mt-3 text-center text-[11px] text-slate-500">SM-2 interval ও next review date এই device-এ save হয়।</p></div>}</> : <div className="panel p-12 text-center"><h3 className="text-lg font-semibold text-white">No cards in this set</h3><p className="mt-2 text-sm text-slate-500">সব question দেখো অথবা কিছু question bookmark করে এই set-এ ফিরো।</p><button onClick={() => setFilter("all")} className="mt-5 rounded-xl bg-mint px-4 py-2.5 text-sm font-bold text-ink">Show all cards</button></div>}
  </div>;
}''',
"components/ProgressDashboard.tsx": r'''"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import type { QuestionIndexItem, ProgressMap, ProgressStatus } from "@/types";
import { ProgressChart } from "@/components/ProgressChart";
import { formatDate } from "@/lib/utils";
import { getCurrentStreak, readActivity, readProgress, saveStatus } from "@/lib/progress";

const statusOptions: { value: ProgressStatus; label: string; color: string }[] = [
  { value: "todo", label: "To do", color: "bg-slate-400" },
  { value: "in-progress", label: "In progress", color: "bg-sky-400" },
  { value: "solved", label: "Solved", color: "bg-emerald-400" },
  { value: "needs-review", label: "Needs review", color: "bg-amber-300" }
];

export function ProgressDashboard({ questions }: { questions: QuestionIndexItem[] }) {
  const [progress, setProgress] = useState<ProgressMap>({});
  const [activity, setActivity] = useState<string[]>([]);
  const [filter, setFilter] = useState<ProgressStatus | "all" | "due">("all");
  const [search, setSearch] = useState("");
  const [revision, setRevision] = useState(0);
  useEffect(() => { setProgress(readProgress()); setActivity(readActivity()); }, [revision]);
  const counts = useMemo(() => {
    const result: Record<ProgressStatus, number> = { todo: 0, "in-progress": 0, solved: 0, "needs-review": 0 };
    for (const question of questions) result[progress[question.slug]?.status || "todo"] += 1;
    return result;
  }, [progress, questions]);
  const dueCount = useMemo(() => questions.filter((question) => {
    const due = progress[question.slug]?.nextReview;
    return !due || new Date(due).getTime() <= Date.now();
  }).length, [progress, questions]);
  const filtered = useMemo(() => questions.filter((question) => {
    const status = progress[question.slug]?.status || "todo";
    const due = progress[question.slug]?.nextReview;
    const statusMatch = filter === "all" || filter === status || (filter === "due" && (!due || new Date(due).getTime() <= Date.now()));
    return statusMatch && `${question.title} ${question.topic}`.toLowerCase().includes(search.toLowerCase());
  }).slice(0, 30), [filter, progress, questions, search]);
  const chart = statusOptions.map((option) => ({ label: option.label, value: counts[option.value], color: option.color }));
  const streak = getCurrentStreak(activity);
  function update(slug: string, status: ProgressStatus) { saveStatus(slug, status); setRevision((value) => value + 1); }

  return <div className="space-y-6">
    <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">{[{ label: "Solved", value: counts.solved, note: `${Math.round(counts.solved / Math.max(1, questions.length) * 100)}% of library`, color: "text-mint" }, { label: "In progress", value: counts["in-progress"], note: "Currently working on", color: "text-sky" }, { label: "Due to review", value: dueCount, note: "Spaced repetition queue", color: "text-amber" }, { label: "Day streak", value: streak, note: "Study days in a row", color: "text-white" }].map((item) => <div key={item.label} className="panel p-5"><p className="text-xs text-slate-500">{item.label}</p><p className={`mt-2 text-3xl font-bold tabular-nums ${item.color}`}>{item.value}</p><p className="mt-2 text-xs text-slate-600">{item.note}</p></div>)}</div>
    <div className="grid gap-5 lg:grid-cols-[0.8fr_1.2fr]"><ProgressChart data={chart} total={questions.length} /><div className="panel p-5"><div className="flex items-center justify-between gap-3"><h3 className="font-semibold text-slate-100">Study activity</h3><span className="text-xs text-slate-500">Last 14 days</span></div><div className="mt-5 grid grid-cols-7 gap-2 sm:grid-cols-14">{Array.from({ length: 14 }, (_, index) => { const day = new Date(); day.setDate(day.getDate() - (13 - index)); const key = day.toISOString().slice(0, 10); const active = activity.includes(key); return <div key={key} className="text-center"><div title={`${key}${active ? " · studied" : " · no activity"}`} className={`mx-auto aspect-square w-full max-w-8 rounded-md border ${active ? "border-mint/20 bg-mint/70" : "border-white/[0.05] bg-white/[0.035]"}`} /><span className="mt-2 block text-[9px] text-slate-600">{day.getDate()}</span></div>; })}</div><p className="mt-4 text-xs leading-5 text-slate-500">কোনো question পড়া, bookmark করা, note save বা review rate করলে activity record হয়। Data শুধু এই browser-এ রাখা হয়।</p></div></div>
    <div className="panel p-5"><div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between"><div><h3 className="text-lg font-semibold text-white">Question tracker</h3><p className="mt-1 text-xs text-slate-500">Status এবং review schedule এই device-এ save হয়।</p></div><label className="text-xs text-slate-500">Find a question<input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search title or topic" className="mt-2 block w-full rounded-xl border border-white/10 bg-[#0b101c] px-3 py-2.5 text-sm text-slate-200 outline-none sm:w-56" /></label></div>
      <div className="mt-4 flex flex-wrap gap-2">{[{ value: "all", label: "All" }, ...statusOptions.map((item) => ({ value: item.value, label: item.label })), { value: "due", label: "Due for review" }].map((item) => <button key={item.value} onClick={() => setFilter(item.value as typeof filter)} className={`rounded-lg border px-3 py-2 text-xs font-semibold ${filter === item.value ? "border-mint/30 bg-mint/10 text-mint" : "border-white/10 text-slate-500 hover:text-slate-200"}`}>{item.label}</button>)}</div>
      <div className="mt-4 divide-y divide-white/[0.06]">{filtered.map((question) => { const record = progress[question.slug]; const status = record?.status || "todo"; return <div key={question.slug} className="flex flex-col gap-3 py-3 sm:flex-row sm:items-center sm:justify-between"><div className="min-w-0"><Link href={`/questions/${question.slug}/`} className="text-sm font-semibold text-slate-200 hover:text-mint">{question.title}</Link><p className="mt-1 text-xs text-slate-600">{question.topic} · Next review: {formatDate(record?.nextReview || null)}</p></div><select aria-label={`Status for ${question.title}`} value={status} onChange={(event) => update(question.slug, event.target.value as ProgressStatus)} className="rounded-lg border border-white/10 bg-[#0b101c] px-3 py-2 text-xs text-slate-300"><option value="todo">To do</option><option value="in-progress">In progress</option><option value="solved">Solved</option><option value="needs-review">Needs review</option></select></div>; })}</div>
      {filtered.length === 0 && <p className="py-8 text-center text-sm text-slate-500">No matching questions.</p>}
      {questions.length > filtered.length && <p className="mt-3 text-center text-[11px] text-slate-600">Showing up to 30 matches. Use search to narrow the list.</p>}
    </div>
  </div>;
}''',
"components/Community.tsx": r'''"use client";

const repo = process.env.NEXT_PUBLIC_GISCUS_REPO || "rafahim/interviewprep-bd";
const repoId = process.env.NEXT_PUBLIC_GISCUS_REPO_ID || "";
const category = process.env.NEXT_PUBLIC_GISCUS_CATEGORY || "General";
const categoryId = process.env.NEXT_PUBLIC_GISCUS_CATEGORY_ID || "";

export function Community({ slug }: { slug?: string }) {
  const discussion = `https://github.com/${repo}/discussions`;
  const configured = Boolean(repoId && categoryId);
  const giscus = `https://giscus.app/iframe.html?origin=https%3A%2F%2Frafahim.com&session=&repo=${encodeURIComponent(repo)}&repoId=${encodeURIComponent(repoId)}&category=${encodeURIComponent(category)}&categoryId=${encodeURIComponent(categoryId)}&mapping=${encodeURIComponent(slug ? "specific" : "pathname")}&term=${encodeURIComponent(slug || "")}&strict=0&reactionsEnabled=1&emitMetadata=0&inputPosition=top&theme=dark&lang=bn`;
  return <section className="panel p-5 sm:p-6"><div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between"><div><p className="text-[10px] font-bold uppercase tracking-[0.16em] text-mint">Community</p><h3 className="mt-2 text-lg font-semibold text-white">Improve the question bank</h3><p className="mt-2 max-w-xl text-sm leading-6 text-slate-400">Correction, better explanation, translation or a new question যোগ করতে GitHub Pull Request খুলো। Discussion-এর জন্য Giscus configure করা যায়।</p></div><a href={`https://github.com/${repo}/pulls`} target="_blank" rel="noreferrer" className="shrink-0 rounded-xl border border-white/10 px-4 py-2.5 text-xs font-bold text-slate-200 transition hover:border-mint/30 hover:text-mint">Open a GitHub PR ↗</a></div>{configured ? <div className="mt-6 overflow-hidden rounded-xl border border-white/10 bg-[#080d17]"><iframe title="Giscus community discussion" src={giscus} loading="lazy" className="h-[420px] w-full border-0" /></div> : <div className="mt-5 rounded-xl border border-dashed border-white/10 bg-white/[0.02] p-4"><p className="text-sm font-semibold text-slate-300">Comments are optional</p><p className="mt-1 text-xs leading-5 text-slate-500">Set `NEXT_PUBLIC_GISCUS_REPO_ID` and `NEXT_PUBLIC_GISCUS_CATEGORY_ID` in your deployment environment to enable Giscus. Until then, the repo Discussions link remains available.</p><a href={discussion} target="_blank" rel="noreferrer" className="mt-3 inline-block text-xs font-semibold text-sky hover:text-mint">Open GitHub Discussions ↗</a></div>}</section>;
}''',
"app/api/questions/route.ts": r'''import { NextResponse } from "next/server";
import { getQuestionIndex } from "@/lib/questions";

export const dynamic = "force-static";

export async function GET() {
  return NextResponse.json(getQuestionIndex(), { headers: { "Cache-Control": "public, max-age=3600, s-maxage=86400" } });
}''',
"app/api/feedback/route.ts": r'''import { NextResponse } from "next/server";
import { getAllQuestions } from "@/lib/questions";
import { getSupabaseAdmin } from "@/lib/supabase";

export async function POST(request: Request) {
  let payload: { slug?: string; rating?: string };
  try {
    payload = await request.json();
  } catch {
    return NextResponse.json({ error: "Invalid JSON body." }, { status: 400 });
  }
  if (!payload.slug || !["helpful", "needs-work"].includes(payload.rating || "")) {
    return NextResponse.json({ error: "A valid slug and rating are required." }, { status: 400 });
  }
  if (!getAllQuestions().some((question) => question.slug === payload.slug)) {
    return NextResponse.json({ error: "Question not found." }, { status: 404 });
  }
  const supabase = getSupabaseAdmin();
  if (!supabase) return NextResponse.json({ ok: true, persisted: false });
  const { error } = await supabase.from("question_feedback").insert({ slug: payload.slug, rating: payload.rating });
  if (error) return NextResponse.json({ error: "Feedback storage is not configured correctly." }, { status: 503 });
  return NextResponse.json({ ok: true, persisted: true });
}''',
"app/api/health/route.ts": r'''import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({ status: "ok", app: "InterviewPrep BD", owner: "RA Fahim" });
}'''
})

FILES.update({
"app/page.tsx": r'''import Link from "next/link";
import type { Metadata } from "next";
import { getQuestionIndex } from "@/lib/questions";
import { CATEGORY_DESCRIPTIONS, CATEGORY_LABELS, CATEGORY_ORDER } from "@/lib/categories";
import { QuestionCard } from "@/components/QuestionCard";
import { Community } from "@/components/Community";
import { SITE_URL, DEFAULT_DESCRIPTION, KEYWORDS } from "@/lib/seo";

export const metadata: Metadata = {
  title: { absolute: "InterviewPrep BD — Free Coding Interview Prep in Bengali | RA Fahim" },
  description: DEFAULT_DESCRIPTION,
  keywords: KEYWORDS,
  authors: [{ name: "RA Fahim", url: "https://rafahim.com" }],
  creator: "RA Fahim",
  alternates: { canonical: `${SITE_URL}/` },
  openGraph: { type: "website", locale: "en_BD", url: `${SITE_URL}/`, siteName: "InterviewPrep BD", title: "InterviewPrep BD — Free Coding Interview Prep in Bengali | RA Fahim", description: DEFAULT_DESCRIPTION, images: [{ url: `${SITE_URL}/og-image.svg`, width: 1200, height: 630, alt: "InterviewPrep BD by RA Fahim" }] },
  twitter: { card: "summary_large_image", creator: "@rafahimn", title: "InterviewPrep BD — Free Coding Interview Prep in Bengali | RA Fahim", description: DEFAULT_DESCRIPTION, images: [`${SITE_URL}/og-image.svg`] }
};

export default function HomePage() {
  const questions = getQuestionIndex();
  const featured = ["two-sum", "url-shortener", "acid-transactions", "tell-me-about-yourself", "javascript-event-loop", "bd-salary-expectation"].map((slug) => questions.find((question) => question.slug === slug)).filter((question) => question !== undefined);
  const schema = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "name": "InterviewPrep BD interview question bank",
    "numberOfItems": questions.length,
    "itemListElement": questions.map((question, index) => ({ "@type": "ListItem", position: index + 1, name: question.title, url: `${SITE_URL}/questions/${question.slug}/` }))
  };
  return <>
    <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />
    <section className="relative overflow-hidden border-b border-white/[0.06]">
      <div className="soft-grid absolute inset-0 opacity-40" /><div className="absolute -right-40 -top-48 h-[520px] w-[520px] rounded-full bg-mint/[0.07] blur-3xl" />
      <div className="relative mx-auto grid max-w-7xl gap-12 px-5 py-16 sm:px-8 sm:py-24 lg:grid-cols-[1.15fr_0.85fr] lg:items-center lg:py-28">
        <div><span className="inline-flex items-center gap-2 rounded-full border border-mint/20 bg-mint/[0.06] px-3 py-1.5 text-[11px] font-semibold tracking-wide text-mint"><span className="h-1.5 w-1.5 rounded-full bg-mint" /> Free forever · Made in Bangladesh</span><h1 className="mt-6 max-w-3xl text-4xl font-bold leading-[1.08] tracking-[-0.045em] text-white sm:text-6xl">Crack your next interview.<br /><span className="text-mint">নিজের ভাষায় শেখো।</span></h1><p className="mt-6 max-w-2xl text-base leading-8 text-slate-400 sm:text-lg">DSA, System Design, Database, behavioral এবং Bangladesh tech interview—সব এক জায়গায়। প্রতিটি প্রশ্নে পরিষ্কার বাংলা explanation, complexity, edge cases এবং practice workflow.</p><div className="mt-8 flex flex-wrap gap-3"><Link href="/questions/" className="rounded-xl bg-mint px-5 py-3.5 text-sm font-bold text-ink shadow-glow transition hover:bg-white">Explore questions <span aria-hidden="true">→</span></Link><Link href="/practice/" className="rounded-xl border border-white/10 bg-white/[0.03] px-5 py-3.5 text-sm font-semibold text-slate-200 transition hover:border-white/20 hover:bg-white/[0.06]">Start a mock interview</Link></div><div className="mt-8 flex flex-wrap items-center gap-x-5 gap-y-2 text-xs text-slate-500"><span>⌘K quick search</span><span>Local-first progress</span><span>Python + JavaScript solutions</span></div></div>
        <div className="relative"><div className="absolute -inset-4 rounded-[2rem] bg-gradient-to-br from-mint/[0.08] via-transparent to-sky/[0.08] blur-2xl" /><div className="panel relative p-5 shadow-glow sm:p-6"><div className="flex items-center justify-between border-b border-white/[0.07] pb-4"><div><p className="text-xs text-slate-500">Your prep workspace</p><p className="mt-1 text-lg font-semibold text-white">One habit at a time</p></div><span className="rounded-xl bg-mint/10 px-3 py-2 text-xs font-bold text-mint">IPBD / 2026</span></div><div className="mt-5 grid grid-cols-2 gap-3"><div className="rounded-xl border border-white/[0.07] bg-white/[0.025] p-4"><p className="text-xs text-slate-500">Question bank</p><p className="mt-2 text-3xl font-bold text-white">{questions.length}</p><p className="mt-1 text-[11px] text-slate-600">Written lessons</p></div><div className="rounded-xl border border-white/[0.07] bg-white/[0.025] p-4"><p className="text-xs text-slate-500">Categories</p><p className="mt-2 text-3xl font-bold text-white">06</p><p className="mt-1 text-[11px] text-slate-600">From DSA to career</p></div></div><div className="mt-4 space-y-3">{[{n:"01",t:"Understand the pattern",s:"বাংলায় concept পরিষ্কার করো",w:"w-[92%]"},{n:"02",t:"Practice under time",s:"Timer, note, self-rating",w:"w-[68%]"},{n:"03",t:"Review at the right time",s:"SM-2 spaced repetition",w:"w-[44%]"}].map((item) => <div key={item.n} className="rounded-xl border border-white/[0.06] p-3.5"><div className="flex items-center gap-3"><span className="font-mono text-xs text-mint">{item.n}</span><div className="min-w-0 flex-1"><p className="text-sm font-semibold text-slate-200">{item.t}</p><p className="mt-1 text-xs text-slate-500">{item.s}</p></div><span className="text-xs text-slate-600">↗</span></div><div className="mt-3 h-1 overflow-hidden rounded-full bg-white/[0.05]"><div className={`h-full rounded-full bg-gradient-to-r from-mint to-sky ${item.w}`} /></div></div>)}</div></div></div>
      </div>
    </section>
    <section className="mx-auto max-w-7xl px-5 py-14 sm:px-8"><div className="flex flex-wrap items-end justify-between gap-4"><div><p className="text-xs font-bold uppercase tracking-[0.18em] text-mint">Explore the library</p><h2 className="mt-2 text-2xl font-bold tracking-tight text-white sm:text-3xl">Six tracks. One clear path.</h2><p className="mt-2 max-w-xl text-sm leading-6 text-slate-500">যে role-এর জন্য প্রস্তুতি নিচ্ছো, সে অনুযায়ী topic বেছে নাও।</p></div><Link href="/questions/" className="text-sm font-semibold text-sky hover:text-mint">Browse all questions ↗</Link></div><div className="mt-7 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">{CATEGORY_ORDER.map((category) => { const count = questions.filter((question) => question.category === category).length; return <Link href={`/questions/?category=${category}`} key={category} className="group panel p-5 transition hover:-translate-y-0.5 hover:border-mint/25"><div className="flex items-center justify-between"><span className="flex h-10 w-10 items-center justify-center rounded-xl border border-mint/15 bg-mint/[0.06] font-mono text-xs font-bold text-mint">{String(count).padStart(2, "0")}</span><span className="text-slate-600 transition group-hover:translate-x-1 group-hover:text-mint">↗</span></div><h3 className="mt-4 text-lg font-semibold text-slate-100 group-hover:text-mint">{CATEGORY_LABELS[category]}</h3><p className="mt-2 text-sm leading-6 text-slate-500">{CATEGORY_DESCRIPTIONS[category]}</p><p className="mt-4 text-xs text-slate-600">{count} lessons</p></Link>; })}</div></section>
    <section className="mx-auto max-w-7xl px-5 py-5 sm:px-8"><div className="flex flex-wrap items-end justify-between gap-4"><div><p className="text-xs font-bold uppercase tracking-[0.18em] text-mint">Start here</p><h2 className="mt-2 text-2xl font-bold tracking-tight text-white sm:text-3xl">A few high-value questions</h2></div><Link href="/questions/" className="text-sm font-semibold text-sky hover:text-mint">Full question bank →</Link></div><div className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-3">{featured.map((question) => question ? <QuestionCard key={question.slug} question={question} /> : null)}</div></section>
    <section className="mx-auto max-w-7xl px-5 pt-12 sm:px-8"><div className="grid gap-4 md:grid-cols-3">{[{n:"01",t:"Learn",d:"প্রতিটি lesson-এ concept, complexity, edge case এবং বাস্তব trade-off বোঝো।"},{n:"02",t:"Practice",d:"Timer চালাও, notes লেখো, নিজের performance rate করো।"},{n:"03",t:"Remember",d:"SM-2 spaced repetition দিয়ে ভুলে যাওয়ার আগে আবার review করো।"}].map((item) => <div key={item.n} className="flex gap-4 rounded-2xl border border-white/[0.06] p-5"><span className="font-mono text-sm text-mint">{item.n}</span><div><h3 className="font-semibold text-slate-100">{item.t}</h3><p className="mt-2 text-sm leading-6 text-slate-500">{item.d}</p></div></div>)}</div></section>
    <section className="mx-auto max-w-7xl px-5 pt-12 sm:px-8"><Community /></section>
    <section className="mx-auto max-w-7xl px-5 pb-8 pt-14 sm:px-8"><div className="relative overflow-hidden rounded-3xl border border-mint/15 bg-gradient-to-br from-mint/[0.07] via-panel to-sky/[0.05] p-7 sm:p-10"><div className="absolute -right-12 -top-20 h-64 w-64 rounded-full bg-mint/[0.07] blur-3xl" /><div className="relative flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between"><div><p className="text-xs font-bold uppercase tracking-[0.18em] text-mint">Free. Open. Community-built.</p><h2 className="mt-3 text-2xl font-bold text-white sm:text-3xl">Make the next interview count.</h2><p className="mt-2 max-w-xl text-sm leading-6 text-slate-400">Content ভুল পেলে ঠিক করো, নতুন প্রশ্ন যোগ করো, আর নিজের progress track করো—কোনো account বাধ্যতামূলক নয়।</p></div><Link href="/practice/" className="relative shrink-0 rounded-xl bg-mint px-5 py-3.5 text-sm font-bold text-ink transition hover:bg-white">Start practicing →</Link></div></div></section>
  </>;
}''',
"app/questions/page.tsx": r'''import type { Metadata } from "next";
import { QuestionBrowser } from "@/components/QuestionBrowser";
import { Community } from "@/components/Community";
import { getQuestionIndex } from "@/lib/questions";
import { pageMetadata, SITE_URL } from "@/lib/seo";

export const metadata: Metadata = pageMetadata("Question Bank", "Browse 60 interview questions with Bengali explanations, difficulty, company, language and topic filters.", "/questions/");

export default function QuestionsPage({ searchParams }: { searchParams: { category?: string } }) {
  const questions = getQuestionIndex();
  const initialCategory = CATEGORY_ORDER.find((category) => category === searchParams?.category) || "";
  const schema = { "@context": "https://schema.org", "@type": "ItemList", name: "InterviewPrep BD Question Bank", numberOfItems: questions.length, itemListElement: questions.map((question, index) => ({ "@type": "ListItem", position: index + 1, name: question.title, url: `${SITE_URL}/questions/${question.slug}/` })) };
  return <div className="mx-auto max-w-7xl px-5 py-10 sm:px-8 sm:py-14"><script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} /><div className="max-w-3xl"><p className="text-xs font-bold uppercase tracking-[0.18em] text-mint">Question bank / প্রশ্নভান্ডার</p><h1 className="mt-3 text-3xl font-bold tracking-tight text-white sm:text-5xl">Find the right question.</h1><p className="mt-4 text-sm leading-7 text-slate-400 sm:text-base">Difficulty, topic, company, language এবং frequency দিয়ে filter করো। প্রতিটি lesson-এ Bengali explanation, interview reasoning এবং relevant edge cases রয়েছে।</p></div><div className="mt-8"><QuestionBrowser questions={questions} initialCategory={initialCategory} /></div><div className="mt-12"><Community /></div></div>;
}''',
"app/questions/[slug]/page.tsx": r'''import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { compileMDX } from "next-mdx-remote/rsc";
import rehypePrettyCode from "rehype-pretty-code";
import { QuestionActions } from "@/components/QuestionActions";
import { QuestionCard } from "@/components/QuestionCard";
import { Community } from "@/components/Community";
import { CATEGORY_LABELS } from "@/lib/categories";
import { getAllQuestions, getQuestionBySlug, getQuestionIndex } from "@/lib/questions";
import { difficultyTone } from "@/lib/utils";
import { pageMetadata, SITE_URL } from "@/lib/seo";

export function generateStaticParams() {
  return getAllQuestions().map((question) => ({ slug: question.slug }));
}

export async function generateMetadata({ params }: { params: { slug: string } }): Promise<Metadata> {
  const question = getQuestionBySlug(params.slug);
  if (!question) return pageMetadata("Question Not Found", "The requested interview question could not be found.", "/questions/");
  return pageMetadata(question.title, question.problem, `/questions/${question.slug}/`);
}

export default async function QuestionDetailPage({ params }: { params: { slug: string } }) {
  const question = getQuestionBySlug(params.slug);
  if (!question) notFound();
  const { content } = await compileMDX({
    source: question.content,
    options: { mdxOptions: { rehypePlugins: [[rehypePrettyCode, { theme: "github-dark", keepBackground: false }]] } }
  });
  const all = getQuestionIndex();
  const related = question.related.map((slug) => all.find((item) => item.slug === slug)).filter((item) => item !== undefined).slice(0, 3);
  const schema = {
    "@context": "https://schema.org",
    "@type": "TechArticle",
    headline: question.title,
    description: question.problem,
    inLanguage: ["bn", "en"],
    url: `${SITE_URL}/questions/${question.slug}/`,
    author: { "@type": "Person", name: "RA Fahim", url: "https://rafahim.com" },
    publisher: { "@type": "Organization", name: "InterviewPrep BD", url: `${SITE_URL}/` },
    keywords: question.tags.join(", ")
  };
  return <div className="mx-auto max-w-7xl px-5 py-8 sm:px-8 sm:py-12"><script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} /><div className="mb-7 flex flex-wrap items-center gap-2 text-xs text-slate-600"><Link href="/questions/" className="hover:text-mint">Question bank</Link><span>/</span><span>{CATEGORY_LABELS[question.category]}</span><span>/</span><span className="text-slate-400">{question.title}</span></div><div className="grid gap-8 lg:grid-cols-[minmax(0,1fr)_300px]"><main className="min-w-0"><div className="flex flex-wrap items-center gap-2"><span className="rounded-full border border-white/10 bg-white/[0.03] px-3 py-1.5 text-[11px] font-semibold text-slate-300">{CATEGORY_LABELS[question.category]}</span><span className={`rounded-full border px-3 py-1.5 text-[11px] font-semibold ${difficultyTone(question.difficulty)}`}>{question.difficulty}</span><span className="rounded-full border border-white/10 px-3 py-1.5 text-[11px] text-slate-500">{question.minutes} min</span><span className="rounded-full border border-white/10 px-3 py-1.5 text-[11px] text-slate-500">{question.frequency} frequency</span></div><h1 className="mt-5 text-3xl font-bold leading-tight tracking-tight text-white sm:text-5xl">{question.title}</h1><p className="mt-4 max-w-3xl text-base leading-8 text-slate-400">{question.problem}</p><div className="mt-5 flex flex-wrap gap-2">{question.companies.map((company) => <span key={company} className="rounded-lg border border-white/[0.07] bg-white/[0.025] px-2.5 py-1.5 text-[11px] text-slate-500">{company}</span>)}{question.languages.map((language) => <span key={language} className="rounded-lg border border-sky/15 bg-sky/[0.04] px-2.5 py-1.5 text-[11px] text-sky">{language}</span>)}</div><div className="mt-8 rounded-2xl border border-white/[0.07] bg-[#0a0f1a]/80 p-5 sm:p-7"><article className="prose prose-invert max-w-none">{content}</article></div><div className="mt-8"><Community slug={question.slug} /></div>{related.length > 0 && <section className="mt-10"><div className="flex items-end justify-between gap-4"><div><p className="text-xs font-bold uppercase tracking-[0.16em] text-mint">Keep learning</p><h2 className="mt-2 text-xl font-bold text-white">Related questions</h2></div><Link href="/questions/" className="text-xs font-semibold text-sky hover:text-mint">All questions ↗</Link></div><div className="mt-4 grid gap-3 md:grid-cols-3">{related.map((item) => <QuestionCard key={item.slug} question={item} />)}</div></section>}<div className="mt-10 flex items-center justify-between border-t border-white/[0.07] pt-5"><Link href="/questions/" className="text-sm font-semibold text-slate-400 hover:text-mint">← Back to question bank</Link><a href="https://github.com/rafahim" target="_blank" rel="noreferrer" className="text-xs text-slate-600 hover:text-slate-300">Improve this lesson ↗</a></div></main><aside className="space-y-4 lg:sticky lg:top-28 lg:self-start"><QuestionActions slug={question.slug} title={question.title} content={`${question.problem}\n\n${question.approach}`} /><div className="panel p-4"><p className="text-[10px] font-bold uppercase tracking-[0.15em] text-slate-500">Quick facts</p><div className="mt-3 space-y-3 text-xs">{question.category === "dsa" ? <><div className="flex justify-between gap-3"><span className="text-slate-500">Time complexity</span><span className="text-right font-mono text-slate-200">{question.complexity.time}</span></div><div className="flex justify-between gap-3"><span className="text-slate-500">Extra space</span><span className="text-right font-mono text-slate-200">{question.complexity.space}</span></div></> : <><div className="flex justify-between gap-3"><span className="text-slate-500">Topic</span><span className="text-right text-slate-200">{question.topic}</span></div><div className="flex justify-between gap-3"><span className="text-slate-500">Focus</span><span className="text-right text-slate-200">{question.complexity.space}</span></div></>}<div className="flex justify-between gap-3"><span className="text-slate-500">Study target</span><span className="text-slate-200">{question.minutes} min</span></div></div></div><div className="rounded-2xl border border-sky/15 bg-sky/[0.04] p-4"><p className="text-sm font-semibold text-sky">Interview tip</p><p className="mt-2 text-xs leading-6 text-slate-400">প্রথমে explanation না দেখে solve করার চেষ্টা করো। তারপর invariant, edge cases এবং complexity নিজের ভাষায় explain করো।</p></div></aside></div></div>;
}''',
"app/practice/page.tsx": r'''import type { Metadata } from "next";
import { PracticeRoom } from "@/components/PracticeRoom";
import { getQuestionIndex } from "@/lib/questions";
import { pageMetadata } from "@/lib/seo";

export const metadata: Metadata = pageMetadata("Practice Mode", "Timed mock interviews, random question picker, device-local notes and self-rating for interview preparation.", "/practice/");

export default function PracticePage() {
  return <div className="mx-auto max-w-7xl px-5 py-10 sm:px-8 sm:py-14"><div className="mb-8 max-w-3xl"><p className="text-xs font-bold uppercase tracking-[0.18em] text-mint">Practice / অনুশীলন</p><h1 className="mt-3 text-3xl font-bold tracking-tight text-white sm:text-5xl">Train under interview conditions.</h1><p className="mt-4 text-sm leading-7 text-slate-400 sm:text-base">Random prompt, 5-question mock, timer, private notes এবং self-rating—সব progress browser-এ save হয়।</p></div><PracticeRoom questions={getQuestionIndex()} /></div>;
}''',
"app/progress/page.tsx": r'''import type { Metadata } from "next";
import { ProgressDashboard } from "@/components/ProgressDashboard";
import { getQuestionIndex } from "@/lib/questions";
import { pageMetadata } from "@/lib/seo";

export const metadata: Metadata = pageMetadata("Progress Dashboard", "Track solved questions, review dates, study streaks and local-first interview preparation progress.", "/progress/");

export default function ProgressPage() {
  return <div className="mx-auto max-w-7xl px-5 py-10 sm:px-8 sm:py-14"><div className="mb-8 max-w-3xl"><p className="text-xs font-bold uppercase tracking-[0.18em] text-mint">Progress / অগ্রগতি</p><h1 className="mt-3 text-3xl font-bold tracking-tight text-white sm:text-5xl">Small steps, visible progress.</h1><p className="mt-4 text-sm leading-7 text-slate-400 sm:text-base">Solved, in-progress, todo, needs-review, streak এবং due date—আপনার progress server-এ পাঠানো হয় না; এই browser-এই থাকে।</p></div><ProgressDashboard questions={getQuestionIndex()} /></div>;
}''',
"app/flashcards/page.tsx": r'''import type { Metadata } from "next";
import { Flashcards } from "@/components/Flashcards";
import { getQuestionIndex } from "@/lib/questions";
import { pageMetadata } from "@/lib/seo";

export const metadata: Metadata = pageMetadata("Flashcards", "Auto-generated interview recall flashcards with SM-2 spaced repetition and local review scheduling.", "/flashcards/");

export default function FlashcardsPage() {
  return <div className="mx-auto max-w-7xl px-5 py-10 sm:px-8 sm:py-14"><Flashcards questions={getQuestionIndex()} /></div>;
}''',
"app/not-found.tsx": r'''import Link from "next/link";

export default function NotFound() {
  return <div className="mx-auto flex min-h-[55vh] max-w-3xl flex-col items-center justify-center px-5 text-center"><p className="font-mono text-sm text-mint">404 · NOT FOUND</p><h1 className="mt-4 text-3xl font-bold text-white">Question not found</h1><p className="mt-3 text-sm leading-6 text-slate-500">এই URL-এ কোনো lesson পাওয়া যায়নি। Question bank থেকে অন্য একটি বেছে নাও।</p><Link href="/questions/" className="mt-6 rounded-xl bg-mint px-5 py-3 text-sm font-bold text-ink">Browse questions</Link></div>;
}''',
"scripts/generate-sitemap.mjs": r'''import { readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const base = "https://rafahim.com/interview-prep";
const contentRoot = path.join(process.cwd(), "content");
const staticRoutes = ["/", "/questions/", "/practice/", "/progress/", "/flashcards/"];

async function walk(directory) {
  const entries = await readdir(directory, { withFileTypes: true }).catch(() => []);
  const files = [];
  for (const entry of entries) {
    const full = path.join(directory, entry.name);
    if (entry.isDirectory()) files.push(...await walk(full));
    else if (entry.isFile() && entry.name.endsWith(".mdx")) files.push(full);
  }
  return files;
}

const files = await walk(contentRoot);
const slugs = [];
for (const file of files) {
  const source = await readFile(file, "utf8");
  const match = source.match(/^\s*"slug"\s*:\s*"([^"]+)"/m) || source.match(/^slug:\s*([^\n]+)$/m);
  if (match) slugs.push(match[1].trim().replace(/^['"]|['"]$/g, ""));
}
const routes = [...staticRoutes, ...slugs.map((slug) => `/questions/${slug}/`)];
const body = routes.map((route) => `  <url><loc>${base}${route}</loc><changefreq>${route.startsWith("/questions/") ? "monthly" : "weekly"}</changefreq><priority>${route === "/" ? "1.0" : route.startsWith("/questions/") ? "0.7" : "0.8"}</priority></url>`).join("\n");
const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${body}\n</urlset>\n`;
await writeFile(path.join(process.cwd(), "public", "sitemap.xml"), xml, "utf8");
console.log(`Wrote sitemap with ${routes.length} URLs.`);''',
"setup.sh": r'''#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$ROOT/scripts/scaffold.py" --target "$ROOT" --zip "$ROOT/interviewprep-bd.zip"
printf 'Project files refreshed and ZIP created at %s\n' "$ROOT/interviewprep-bd.zip"''',
"setup.ps1": r'''$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = Get-Command py -ErrorAction SilentlyContinue
if ($Python) {
  & py "$Root\scripts\scaffold.py" --target "$Root" --zip "$Root\interviewprep-bd.zip"
} else {
  & python "$Root\scripts\scaffold.py" --target "$Root" --zip "$Root\interviewprep-bd.zip"
}
if ($LASTEXITCODE -ne 0) { throw "Project generation failed." }
Write-Output "Project files refreshed and ZIP created at $Root\interviewprep-bd.zip"''',
"README.md": r'''# InterviewPrep BD

![Made in Bangladesh](https://img.shields.io/badge/Made%20in-Bangladesh-006a4e?style=for-the-badge&labelColor=f42a41)

Free, bilingual coding interview preparation with Bengali explanations, Python and JavaScript DSA solutions, system design walkthroughs, database fundamentals, STAR-based behavioral examples, and Bangladesh-focused interview advice.

**Creator:** RA Fahim · [rafahim.com](https://rafahim.com) · [GitHub](https://github.com/rafahim) · Dhaka, Bangladesh

## Features

- 60 authored MDX lessons across DSA, system design, database, behavioral, programming languages and Bangladesh interview topics.
- Question browser with fuzzy search, Cmd/Ctrl+K quick search, difficulty, category, topic, company, language and frequency filters, plus sorting.
- Question detail pages with Bengali explanations, Python and JavaScript solutions for all 20 DSA questions, complexity, edge cases, related questions, copy/share/bookmark and feedback.
- Practice workspace with random picker, five-question mock sessions, a configurable timer, device-local notes and self-rating.
- Progress dashboard with todo, in-progress, solved and needs-review states, an activity streak, review queue and SM-2 spaced-repetition scheduling.
- Auto-generated flashcards, optional Giscus discussions, GitHub contribution links and optional Supabase feedback storage.
- Next.js 14 App Router, TypeScript, Tailwind CSS, MDX rendering, Fuse.js search, Shiki-powered syntax highlighting and responsive dark UI.
- Static generation for question routes, SEO metadata, canonical URLs, Open Graph/Twitter tags, JSON-LD, robots.txt, sitemap.xml, manifest, humans.txt, security.txt, favicon and OG artwork.
- No account is required for practice. Progress, bookmarks and notes stay in the current browser unless you choose to configure server-side feedback storage.

## Local development

Requirements: Node.js 18.17 or newer and npm. Python 3 is required only for the optional scaffold/ZIP scripts.

```bash
npm install
npm run dev
```

Open `http://localhost:3000/interview-prep/`. The app uses the `/interview-prep` base path to match its canonical URL. Keep that route prefix in your local links and deployment setup.

Build and check before shipping:

```bash
npm run typecheck
npm run build
npm run start
```

The dev and build lifecycle refreshes `public/sitemap.xml` from the MDX files. To refresh it directly:

```bash
npm run generate:sitemap
```

## Repository files

```text
app/                  App Router pages and API routes
components/            Shared UI and client-side interactions
content/               60 authored MDX questions in six categories
lib/                   Content loading, SEO, progress and SM-2 helpers
types/                 Shared TypeScript types
public/                Search engine files, manifest and vector artwork
scripts/               Sitemap generation and project scaffolding
setup.sh               Rebuild the project tree and ZIP on macOS/Linux
setup.ps1              Rebuild the project tree and ZIP on Windows
```

## Content format and MDX template

Create a new `.mdx` file in the relevant `content/<category>/` folder. The frontmatter is JSON-formatted YAML so nested fields remain easy to edit.

```mdx
---
{
  "slug": "example-question",
  "title": "Example Interview Question",
  "category": "dsa",
  "topic": "Arrays",
  "difficulty": "Easy",
  "companies": ["Google", "Amazon"],
  "languages": ["Python", "JavaScript"],
  "frequency": "Medium",
  "minutes": 15,
  "problem": "Write the exact interview prompt here.",
  "approach": "বাংলায় intuition, invariant এবং implementation strategy ব্যাখ্যা করো।",
  "complexity": { "time": "O(n)", "space": "O(n)" },
  "edges": ["Empty input", "Duplicate values"],
  "related": ["two-sum"],
  "front": "What should the learner recall?",
  "back": "A concise, accurate answer in Bengali.",
  "summary": "Search-friendly summary of this lesson.",
  "tags": ["arrays", "hash-map"],
  "examples": { "input": "[2, 7], target = 9", "output": "[0, 1]" },
  "order": 100
}
---

## Problem

Write the complete problem and constraints in clear language.

## Approach বাংলায়

Explain the idea, why it works, and where the trade-offs appear.

## Example

Show input, output and a short walkthrough.

## Complexity

Explain time and auxiliary-space cost.

## Edge cases

List testable edge cases with short explanations.
```

For DSA lessons, include both Python and JavaScript fenced code blocks. Syntax highlighting is produced by Shiki through `rehype-pretty-code`. After adding a question, check `npm run typecheck`, verify the route, and refresh the sitemap.

## Local data and optional Supabase feedback

Bookmarks, progress, notes, activity and review scheduling use browser localStorage. They do not require Supabase.

To persist question feedback, create a Supabase table with a minimal schema such as:

```sql
create table if not exists public.question_feedback (
  id bigint generated by default as identity primary key,
  slug text not null,
  rating text not null check (rating in ('helpful', 'needs-work')),
  created_at timestamptz not null default now()
);
```

Set `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` in the server environment. Never add the service role key to a `NEXT_PUBLIC_` variable or commit a real secret. Enable suitable row-level security and server-only access before using this table in production.

## Giscus community comments

Giscus is optional. Configure these values in the deployment environment after enabling Discussions and installing the Giscus GitHub App for the repository:

- `NEXT_PUBLIC_GISCUS_REPO`
- `NEXT_PUBLIC_GISCUS_REPO_ID`
- `NEXT_PUBLIC_GISCUS_CATEGORY`
- `NEXT_PUBLIC_GISCUS_CATEGORY_ID`

The app shows a GitHub Discussions link until repository and category IDs are provided.

## Vercel deployment

1. Push the repository to GitHub.
2. Import the repository in Vercel and use the default Next.js framework preset.
3. Keep the repository root as the project root; Vercel will install dependencies and run `next build`.
4. Configure the intended URL routing so the app is served at `https://rafahim.com/interview-prep/`. The Next.js `basePath` is intentionally `/interview-prep` to match the canonical URLs. If this repository is deployed as its own Vercel project, route the `/interview-prep` path from the parent site to this deployment using the parent site's rewrite or your hosting platform's path-routing feature.
5. Add optional Giscus/Supabase environment values only when using those integrations.
6. After deployment, open `/interview-prep/robots.txt`, `/interview-prep/sitemap.xml`, and a question URL to confirm the path routing and canonical metadata.

## SEO checklist

- [ ] Keep the title template `%s | InterviewPrep BD by RA Fahim` and the requested home title.
- [ ] Confirm canonical URLs use `https://rafahim.com/interview-prep/` and its child routes.
- [ ] Confirm Open Graph image and Twitter creator `@rafahimn` render correctly.
- [ ] Confirm WebSite, Person, ItemList and TechArticle JSON-LD in rendered HTML.
- [ ] Run `npm run generate:sitemap` after content edits and submit the sitemap in Google Search Console.
- [ ] Check robots.txt, metadata descriptions, headings, internal links and mobile layout.
- [ ] Do not index draft lessons until their content is complete and useful.
- [ ] Add the deployed canonical property to Search Console and verify URL-prefix routing.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md), use the MDX template above, and open a pull request. Prefer practical examples, accurate complexity analysis and clear Bengali explanations. When updating content, make sure the metadata and solution agree.

## Author

**RA Fahim** is a Web Developer & Creator based in Dhaka, Bangladesh, focused on full-stack web development. This project is built as a free resource for learners preparing for coding interviews in Bengali and English.

- Website: [rafahim.com](https://rafahim.com)
- GitHub: [github.com/rafahim](https://github.com/rafahim)
- Email: [dev@rafahim.com](mailto:dev@rafahim.com)
- X: [@rafahimn](https://twitter.com/rafahimn)
- LinkedIn: [rafahimn](https://linkedin.com/in/rafahimn)

## License

MIT. See [LICENSE](LICENSE).
''',
"CONTRIBUTING.md": r'''# Contributing to InterviewPrep BD

Thanks for helping keep interview preparation practical, accurate and accessible in Bengali and English.

## Ways to contribute

- Fix a bug or accessibility issue.
- Improve Bengali wording, examples, edge cases or time/space analysis.
- Add a complete interview question in the appropriate `content/` category.
- Improve search, mobile usability, progress tracking, flashcards or documentation.

## Question quality checklist

1. State a precise prompt and constraints.
2. Include a sample input/output and explain what it demonstrates.
3. Explain the approach in Bengali without skipping the important invariant.
4. For DSA, include correct Python and JavaScript solutions.
5. Check time and auxiliary-space complexity against the actual implementation.
6. Include empty, minimum, duplicate, invalid or boundary cases when relevant.
7. Add concise tags, valid related slugs, company/frequency metadata only when defensible, and a useful flashcard.
8. Keep answers original and do not copy proprietary interview material or personal candidate data.

## Run locally

```bash
npm install
npm run dev
npm run typecheck
npm run build
```

Open `http://localhost:3000/interview-prep/`. Run `npm run generate:sitemap` after adding or renaming content. The new slug should appear in `public/sitemap.xml` and render under `/interview-prep/questions/<slug>/`.

## MDX frontmatter

Use the template in the README. Add the file to the category directory matching its `category` value. Slugs must be unique and lowercase kebab-case. Related slugs must already exist or be added in the same pull request.

## Pull requests

Keep each PR focused. Explain what changed, why it matters, how it was tested and include screenshots for visible UI changes. Do not commit `.env`, keys, generated `.next/`, `node_modules/` or personal data. Review all modified files before requesting review.

## Reporting security issues

Do not post exploitable vulnerabilities or secrets in a public issue. Follow the private reporting instructions in `public/.well-known/security.txt`.
''',
"CODE_OF_CONDUCT.md": r'''# Code of Conduct

## Our commitment

InterviewPrep BD aims to make technical learning welcoming, useful and respectful for people with different backgrounds, experience levels and language preferences.

## Expected behavior

- Be kind, constructive and specific.
- Critique ideas and code, not people.
- Explain corrections without humiliating beginners.
- Respect different communication styles and Bengali/English proficiency.
- Give credit and follow licenses when sharing material.

## Unacceptable behavior

Harassment, threats, discriminatory language, doxxing, sustained personal attacks, spam and sharing private information without consent are not acceptable.

## Maintainer response

Maintainers may edit, reject or remove contributions that violate this code and may block repeated or serious offenders. When reporting a concern, share relevant context without reposting private information publicly.

## Scope

This code applies to project issues, pull requests, discussions and other project spaces. For sensitive concerns, contact dev@rafahim.com.
''',
"LICENSE": r'''MIT License

Copyright (c) 2026 RA Fahim

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.''',
".github/ISSUE_TEMPLATE/bug_report.md": r'''---
name: Bug report
about: Report a reproducible problem in the app or content
title: "[Bug]: "
labels: bug
assignees: ""
---

## What happened?

Describe the issue clearly.

## Steps to reproduce

1. Open …
2. Choose …
3. Observe …

## Expected behavior

Describe what should happen.

## Environment

- Browser and version:
- Device / screen size:
- Route:

## Extra context

Screenshots, console errors or relevant details without secrets or personal data.''',
".github/ISSUE_TEMPLATE/new_lesson.md": r'''---
name: New lesson proposal
about: Propose a complete new interview lesson
title: "[Lesson]: "
labels: content
assignees: ""
---

## Question title

## Category and topic

## Interview prompt and constraints

## Why this lesson adds value

## Approach in Bengali

## Example input and output

## Complexity analysis

## Python and JavaScript solutions, if DSA

## Edge cases

## Suggested related slugs

## Sources or references

Use sources that are allowed to share and do not include private interview material.''',
".github/PULL_REQUEST_TEMPLATE.md": r'''## What changed?

Describe the user-visible or content change.

## Why?

Explain the problem this solves.

## Validation

- [ ] `npm run typecheck`
- [ ] `npm run build`
- [ ] `npm run generate:sitemap` after content changes
- [ ] Tested mobile and desktop for UI changes
- [ ] Checked links, metadata and edge cases

## Screenshots or content notes

Add screenshots or summarize the new lesson(s).''',
".github/FUNDING.yml": r'''custom: ["https://rafahim.com"]''',
"public/robots.txt": r'''User-agent: *
Allow: /
Sitemap: https://rafahim.com/interview-prep/sitemap.xml''',
"public/manifest.json": r'''{
  "name": "InterviewPrep BD by RA Fahim",
  "short_name": "InterviewPrep BD",
  "description": "Free coding interview preparation in Bengali and English.",
  "start_url": "/interview-prep/",
  "scope": "/interview-prep/",
  "display": "standalone",
  "background_color": "#070a12",
  "theme_color": "#070a12",
  "lang": "bn",
  "icons": [{ "src": "/interview-prep/favicon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any maskable" }]
}''',
"public/humans.txt": r'''/* TEAM */
Creator: RA Fahim
Role: Web Developer & Creator
Website: https://rafahim.com
GitHub: https://github.com/rafahim
Email: dev@rafahim.com
Location: Dhaka, Bangladesh

/* SITE */
Standards: HTML5, CSS3, TypeScript
Software: Next.js 14, React, Tailwind CSS, MDX, Fuse.js, Shiki
Content: Bengali and English
Last update: 2026''',
"public/.well-known/security.txt": r'''Contact: mailto:dev@rafahim.com
Canonical: https://rafahim.com/interview-prep/.well-known/security.txt
Preferred-Languages: bn, en
Policy: https://rafahim.com/interview-prep/''',
"public/favicon.svg": r'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="17" fill="#75f0c1"/><path d="M16 19h32v7H24v6h20v7H24v9h-8z" fill="#070a12"/><circle cx="47" cy="46" r="5" fill="#070a12"/></svg>''',
"public/og-image.svg": r'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630"><defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#111b2d"/><stop offset="1" stop-color="#070a12"/></linearGradient><radialGradient id="glow"><stop offset="0" stop-color="#75f0c1" stop-opacity=".19"/><stop offset="1" stop-color="#75f0c1" stop-opacity="0"/></radialGradient></defs><rect width="1200" height="630" fill="url(#bg)"/><circle cx="1010" cy="100" r="380" fill="url(#glow)"/><g opacity=".16" stroke="#9fb0c9"><path d="M0 70H1200M0 140H1200M0 210H1200M0 280H1200M0 350H1200M0 420H1200M0 490H1200M0 560H1200"/><path d="M70 0V630M140 0V630M210 0V630M280 0V630M350 0V630M420 0V630M490 0V630M560 0V630M630 0V630M700 0V630M770 0V630M840 0V630M910 0V630M980 0V630M1050 0V630M1120 0V630"/></g><rect x="78" y="78" width="66" height="66" rx="18" fill="#75f0c1"/><text x="111" y="120" font-family="Arial,sans-serif" font-size="25" font-weight="800" text-anchor="middle" fill="#070a12">IP</text><text x="78" y="226" font-family="Arial,sans-serif" font-size="24" font-weight="700" letter-spacing="5" fill="#75f0c1">FREE INTERVIEW PREP · MADE IN BANGLADESH</text><text x="74" y="319" font-family="Arial,sans-serif" font-size="66" font-weight="800" letter-spacing="-2" fill="#f2f6ff">InterviewPrep <tspan fill="#75f0c1">BD</tspan></text><text x="80" y="382" font-family="Arial,sans-serif" font-size="28" fill="#c0ccdf">Coding · System Design · Databases · Behavioral</text><text x="80" y="442" font-family="Arial,sans-serif" font-size="23" fill="#8c9ab0">বাংলায় শেখো। English interview-এর জন্য প্রস্তুত হও।</text><path d="M80 508H1120" stroke="#fff" stroke-opacity=".12"/><text x="80" y="554" font-family="Arial,sans-serif" font-size="19" font-weight="700" fill="#e9eef8">Built by RA Fahim</text><text x="1118" y="554" font-family="Arial,sans-serif" font-size="19" text-anchor="end" fill="#8c9ab0">rafahim.com/interview-prep</text></svg>'''
})


def question_metadata(q, order, valid_slugs):
    if q['slug'] in EXAMPLES:
        example_input, example_output = EXAMPLES[q['slug']]
    else:
        example_input, example_output = q['problem'], q['back']
    related = [slug for slug in q['related'] if slug in valid_slugs and slug != q['slug']]
    tags = []
    for part in re.split(r"[^a-zA-Z0-9]+", q['topic'].lower()):
        if len(part) > 1 and part not in tags:
            tags.append(part)
    tags.extend([q['category'], q['difficulty'].lower()])
    custom = q['custom']
    return {
        "slug": q['slug'],
        "title": q['title'],
        "category": q['category'],
        "topic": q['topic'],
        "difficulty": q['difficulty'],
        "companies": q['companies'],
        "languages": q['languages'],
        "frequency": q['frequency'],
        "minutes": q['minutes'],
        "problem": q['problem'],
        "approach": q['approach'],
        "complexity": q['complexity'],
        "edges": q['edges'],
        "related": related,
        "front": q['front'],
        "back": q['back'],
        "summary": q['approach'][:220],
        "tags": tags,
        "examples": {"input": example_input, "output": example_output},
        "order": order
    }


def xml_escape(value):
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def generate_sitemap(target: Path):
    routes = ["/", "/questions/", "/practice/", "/progress/", "/flashcards/"] + [f"/questions/{q['slug']}/" for q in questions]
    urls = []
    for route in routes:
        priority = "1.0" if route == "/" else "0.7" if route.startswith("/questions/") else "0.8"
        frequency = "monthly" if route.startswith("/questions/") else "weekly"
        urls.append(f"  <url><loc>{BASE_URL}{route}</loc><changefreq>{frequency}</changefreq><priority>{priority}</priority></url>")
    xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n" + "\n".join(urls) + "\n</urlset>\n"
    (target / "public" / "sitemap.xml").write_text(xml, encoding="utf-8")


def write_project(target: Path, make_zip: str | None = None):
    target.mkdir(parents=True, exist_ok=True)
    files = dict(FILES)
    files["scripts/scaffold.py"] = Path(__file__).read_text(encoding="utf-8")
    for relative, content in files.items():
        output = target / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content.rstrip() + "\n", encoding="utf-8")
    valid_slugs = {q['slug'] for q in questions}
    for order, question in enumerate(questions, start=1):
        metadata = question_metadata(question, order, valid_slugs)
        body = body_for(question).strip()
        source = "---\n" + json.dumps(metadata, ensure_ascii=False, indent=2) + "\n---\n\n" + body + "\n"
        output = target / "content" / question["category"] / f"{question['slug']}.mdx"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(source, encoding="utf-8")
    generate_sitemap(target)
    setup_sh = target / "setup.sh"
    if setup_sh.exists():
        setup_sh.chmod(0o755)
    if make_zip:
        zip_path = Path(make_zip).resolve()
        zip_path.parent.mkdir(parents=True, exist_ok=True)
        if zip_path.exists():
            zip_path.unlink()
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=8) as archive:
            for file in sorted(target.rglob("*")):
                if not file.is_file():
                    continue
                relative = file.relative_to(target)
                if any(part in {"node_modules", ".next", ".git", "out", "coverage"} for part in relative.parts):
                    continue
                if file.suffix == ".zip":
                    continue
                archive.write(file, relative.as_posix())
        print(f"ZIP created: {zip_path}")
    print(f"Project: {target}")
    print(f"Questions: {len(questions)}")
    print(f"Files written: {sum(1 for p in target.rglob('*') if p.is_file())}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default=".")
    parser.add_argument("--zip", default=None)
    args = parser.parse_args()
    write_project(Path(args.target).resolve(), args.zip)

if __name__ == "__main__":
    main()
