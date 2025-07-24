import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# ------------------------- Skills List -------------------------

SKILLS_LIST = [
    # Programming Languages
    "python", "java", "c++", "c", "c#", "javascript", "typescript", "ruby", "go", "swift", "kotlin", "scala", "php", "rust",
    "perl", "shell scripting", "bash", "objective-c", "matlab", "r", "dart", "groovy", "elixir", "haskell", "clojure",

    # Web Development Frameworks & Libraries
    "html", "css", "sass", "less", "react", "angular", "vue", "ember", "backbone", "jquery",
    "node.js", "express", "django", "flask", "spring", "laravel", "symfony", "graphql", "apollo",
    "bootstrap", "tailwind css", "webassembly", "next.js", "nuxt.js", "redux", "gatsby", "jekyll", "webpack", "babel",

    # Databases & Data Storage
    "sql", "mysql", "postgresql", "mongodb", "redis", "oracle", "sqlite", "cassandra", "elasticsearch",
    "firebase", "dynamodb", "microsoft sql server", "neo4j", "hbase", "cockroachdb", "mariadb", "influxdb", "timescaledb",

    # Cloud Platforms & Services
    "aws", "amazon web services", "azure", "google cloud", "gcp", "ibm cloud", "oracle cloud", "digitalocean",
    "heroku", "firebase", "cloudflare", "linode", "rackspace", "aliyun",

    # DevOps, Containerization & Orchestration
    "docker", "kubernetes", "terraform", "ansible", "puppet", "chef", "jenkins", "travis ci", "circleci",
    "gitlab ci", "ci/cd", "helm", "prometheus", "grafana", "elasticsearch stack", "splunk", "new relic",
    "vault", "consul", "linkerd", "istio", "openshift", "argo cd", "spinnaker", "rancher",

    # Operating Systems & Networking
    "linux", "unix", "windows server", "macos", "networking", "tcp/ip", "dns", "dhcp", "vpn", "firewall",
    "load balancing", "proxy", "wireless networking", "network security", "iptables", "wireshark", "nmap", "netcat",

    # Data Science, Machine Learning & AI Tools
    "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn", "keras", "pandas", "numpy",
    "matplotlib", "seaborn", "nlp", "computer vision", "opencv", "data analysis", "data mining", "big data",
    "hadoop", "spark", "apache kafka", "apache flink", "data engineering", "reinforcement learning",
    "unsupervised learning", "supervised learning", "time series analysis", "tensorflow serving", "xgboost",
    "lightgbm", "catboost", "mlflow", "kubeflow", "airflow", "great expectations", "dvc", "tfx",

    # Software Development Practices & Tools
    "agile", "scrum", "kanban", "test-driven development", "tdd", "behavior-driven development", "bdd",
    "rest api", "graphql api", "microservices", "monolithic architecture", "serverless",
    "event-driven architecture", "clean code", "design patterns", "software architecture",
    "performance tuning", "debugging", "version control", "git", "svn", "mercurial", "jira", "confluence",
    "postman", "swagger", "soapui", "fiddler", "selenium", "cypress", "jmeter", "loadrunner",

    # Security Tools & Concepts
    "cybersecurity", "penetration testing", "network security", "application security", "encryption",
    "ssl/tls", "oauth", "jwt", "firewalls", "antivirus", "vulnerability assessment", "threat modeling",
    "security compliance", "gdpr", "hipaa", "wireshark", "burp suite", "metasploit", "nessus", "openvas",
    "snort", "ossec", "kali linux", "chkrootkit",

    # Mobile & Embedded Development
    "android development", "ios development", "flutter", "react native", "xamarin", "embedded systems",
    "arduino", "raspberry pi", "iot", "robotics", "firmware development", "real-time operating systems",
    "qt", "blackberry", "cordova", "phonegap", "unity", "unreal engine", "vuforia",

    # Others / Emerging Technologies
    "blockchain", "cryptocurrency", "smart contracts", "decentralized applications", "virtual reality",
    "augmented reality", "edge computing", "quantum computing", "chatbots", "voice assistants",
    "api design", "multithreading", "concurrency", "parallel computing", "cloud computing",
    "virtualization", "automation", "business intelligence", "data visualization", "etl", "etl pipelines",
    "docker swarm", "openstack", "apache airflow", "elastic stack", "apache hive", "apache pig",
    "apache storm", "spark streaming", "tensorflow lite", "keras tuner", "mlflow", "kubeflow",
    "airflow", "great expectations", "data quality", "data governance", "splunk", "datadog", "new relic",
    "pagerduty", "zabbix", "nagios", "sentry", "rollbar",

    # IDEs and Editors
    "visual studio code", "intellij idea", "eclipse", "pycharm", "android studio", "xcode", "netbeans",
    "sublime text", "vim", "emacs", "atom",

    # Collaboration & Communication
    "slack", "microsoft teams", "zoom", "jira", "confluence", "trello", "asana", "monday.com", "github", "gitlab", "bitbucket",

    # Testing & QA
    "selenium", "cypress", "junit", "pytest", "mocha", "chai", "jest", "karma", "jasmine", "postman", "soapui",
    "loadrunner", "jmeter", "gatling",

    # Containers & Virtualization
    "docker", "podman", "lxc", "vagrant", "virtualbox", "vmware", "hyper-v", "kvm",

    # Monitoring & Logging
    "prometheus", "grafana", "elk stack", "elastic stack", "logstash", "kibana", "fluentd", "graylog", "splunk", "new relic", "datadog",

    # Messaging & Streaming
    "apache kafka", "rabbitmq", "activemq", "mqtt", "zeromq",

    # Automation & Scripting
    "ansible", "puppet", "chef", "saltstack", "terraform", "bash scripting", "powershell",

    # Big Data & Analytics
    "hadoop", "spark", "flink", "hive", "pig", "storm", "kylin", "impala",

    # Business Intelligence & Visualization
    "tableau", "power bi", "qlikview", "looker", "d3.js", "plotly", "superset", "metabase", "apache echarts",

    # API & Integration
    "rest api", "graphql", "soap", "oauth2", "openapi", "swagger", "postman",

    # CRM & ERP
    "salesforce", "sap", "oracle erp", "microsoft dynamics", "zoho crm",

    # Hardware & IoT Platforms
    "arduino", "raspberry pi", "esp32", "nvidia jetson", "intel galileo", "beaglebone",

    # Cloud Native & Service Mesh
    "istio", "linkerd", "envoy", "consul", "open service mesh",

    # Software Containers & Registries
    "docker hub", "harbor", "aws ecr", "gcp container registry", "azure container registry",

    # Message Brokers & Queues
    "rabbitmq", "activemq", "amazon sqs", "google pubsub",

    # CI/CD Tools
    "jenkins", "travis ci", "circleci", "gitlab ci", "azure pipelines", "bamboo",

    # Configuration Management
    "ansible", "puppet", "chef", "saltstack",

    # Miscellaneous
    "oauth", "jwt", "ssl", "tls", "ldap", "active directory", "dns", "dhcp",

]

# ------------------------- Helper Functions -------------------------

def extract_keywords(text):
    doc = nlp(text)
    return {
        token.text.lower()
        for token in doc
        if token.pos_ in ["NOUN", "VERB", "PROPN"] and not token.is_stop and token.is_alpha
    }

def extract_skills(text):
    text_lower = text.lower()
    found_skills = set()
    for skill in SKILLS_LIST:
        if skill in text_lower:
            found_skills.add(skill)
    return found_skills

def highlight_keywords(text, matches, missing, color_matched="green", color_missing="red"):
    words = text.split()
    highlighted = []
    for word in words:
        clean_word = re.sub(r"[^\w\s]", "", word).lower()
        if clean_word in matches:
            highlighted.append(f"<span style='color:{color_matched}; font-weight:bold'>{word}</span>")
        elif clean_word in missing:
            highlighted.append(f"<span style='color:{color_missing};'>{word}</span>")
        else:
            highlighted.append(word)
    return " ".join(highlighted)

def get_top_tfidf_keywords(text, top_n=10):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform([text])
    feature_names = tfidf.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]
    keyword_scores = list(zip(feature_names, scores))
    keyword_scores.sort(key=lambda x: x[1], reverse=True)
    top_keywords = [kw for kw, score in keyword_scores[:top_n]]
    return set(top_keywords)

# ------------------------- Main Page Function -------------------------

def compare_resume_page():
    st.title("📘 Resume vs Job Description Comparison")

    jd_text = st.session_state.get("jd_text", "")
    resumes = st.session_state.get("resume_list", [])

    st.write(f"📝 Job Description length: {len(jd_text)} characters")

    if not resumes:
        st.warning("⚠️ No resumes found. Please upload your resume(s) first.")
        return

    if not jd_text.strip():
        st.warning("⚠️ No job description found. Please enter or upload a job description first.")
        return

    # Updated comparison modes
    comparison_mode = st.radio("🔍 Select Comparison Mode", [
        "Word-to-Word Comparison",
        "Skills Matching Comparison",  # changed here
        "Overall Match Percentage"
    ])

    for idx, (name, resume_text) in enumerate(resumes):
        st.markdown(f"## 📝 Resume: `{name}`")

        # Common TF-IDF Score (used in all cases)
        tfidf = TfidfVectorizer(stop_words='english')
        vectors = tfidf.fit_transform([resume_text, jd_text])
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        tfidf_score_percent = similarity * 100

        if comparison_mode == "Overall Match Percentage":
            st.markdown("### 🎯 Resume Match Accuracy (TF-IDF Cosine Similarity)")
            st.markdown(
                f"<div style='font-size: 28px; color: green; font-weight: bold;'>{tfidf_score_percent:.0f}%</div>",
                unsafe_allow_html=True
            )

        elif comparison_mode == "Skills Matching Comparison":
            jd_skills = extract_skills(jd_text)
            resume_skills = extract_skills(resume_text)

            matched = jd_skills & resume_skills
            missing = jd_skills - resume_skills

            total_skills = len(jd_skills)
            matched_percent = (len(matched) / total_skills) * 100 if total_skills else 0

            st.markdown("### 🎯 Skills Match Percentage")
            st.markdown(
                f"<div style='font-size: 28px; color: green; font-weight: bold;'>{matched_percent:.0f}%</div>",
                unsafe_allow_html=True
            )

            st.markdown("### 🔑 Skills Required in Job Description")
            st.markdown(", ".join(sorted(jd_skills)) or "No skills found.")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("✅ **Matched Skills**")
                st.markdown(", ".join(sorted(matched)) or "No matched skills.")
            with col2:
                st.markdown("❌ **Missing Skills**")
                st.markdown(", ".join(sorted(missing)) or "No missing skills.")

            st.markdown("### 🧾 Resume Highlight")
            st.markdown(highlight_keywords(resume_text, matched, set()), unsafe_allow_html=True)

            st.markdown("### 📄 Job Description Highlight")
            st.markdown(highlight_keywords(jd_text, matched, missing), unsafe_allow_html=True)

        elif comparison_mode == "Word-to-Word Comparison":
            resume_words = set(re.sub(r'[^\w\s]', '', resume_text.lower()).split())
            jd_words = set(re.sub(r'[^\w\s]', '', jd_text.lower()).split())

            matched_words = jd_words & resume_words
            missing_words = jd_words - resume_words

            total_words = len(jd_words)
            match_percent = (len(matched_words) / total_words) * 100 if total_words else 0

            st.markdown("### 🎯 Word Match Percentage")
            st.markdown(
                f"<div style='font-size: 28px; color: green; font-weight: bold;'>{match_percent:.0f}%</div>",
                unsafe_allow_html=True
            )

            st.markdown("### ✅ Exact Matched Words")
            st.markdown(", ".join(sorted(matched_words)) or "No matched words.")

            st.markdown("### ❌ Missing Words from Job Description")
            st.markdown(", ".join(sorted(missing_words)) or "No missing words.")

            st.markdown("### 🧾 Resume Highlight")
            st.markdown(highlight_keywords(resume_text, matched_words, set()), unsafe_allow_html=True)

            st.markdown("### 📄 Job Description Highlight")
            st.markdown(highlight_keywords(jd_text, matched_words, missing_words), unsafe_allow_html=True)

        # Save for Resume Optimizer
        if idx == 0:
            st.session_state.selected_resume = resume_text
            st.session_state.selected_jd = jd_text
            st.session_state.missing_keywords = list(
                missing_words if comparison_mode == "Word-to-Word Comparison"
                else missing if comparison_mode == "Skills Matching Comparison"
                else []
            )

        if st.button(f"🚀 Improve Resume: {name}", key=f"improve_resume_{idx}"):
            st.session_state.selected_resume = resume_text
            st.session_state.selected_jd = jd_text
            st.session_state.missing_keywords = list(
                missing_words if comparison_mode == "Word-to-Word Comparison"
                else missing if comparison_mode == "Skills Matching Comparison"
                else []
            )
            st.session_state.page = "📄 Resume Optimizer"
            st.experimental_rerun()

        st.markdown("---")

    if st.button("⬅️ Back to Dashboard"):
        st.session_state.page = "📈 Dashboard"
        st.experimental_rerun()
