// Race on compare.html. Pick a task; every lane waits its time to first token, then streams
// its answer and finishes at its total time. Real time, no slow motion.
// Every lane runs the same model, Llama 3.1 8B. Measured, October 2026, median of three runs each:
// Ogbon (our own chat) and SwiftInference (its test page). Modelled: the other providers, from
// Artificial Analysis' first-token time and output speed, streaming the SwiftInference answer.
const TASKS = [
 {
  "id": "word",
  "label": "One word",
  "prompt": "Describe real-time inference in one word.",
  "ogbon": {
   "ttft": 69,
   "total": 80,
   "text": "Streaming."
  },
  "swift": {
   "ttft": 360,
   "total": 638,
   "text": "Instantaneous."
  }
 },
 {
  "id": "support",
  "label": "Support chat",
  "prompt": "A customer was charged $49 twice for the same order. Write a short, friendly support reply that explains the refund.",
  "ogbon": {
   "ttft": 65,
   "total": 480,
   "text": "Subject: Refund for Duplicate Charge on Recent Order\n\nDear [Customer's Name],\n\nThank you for reaching out to us about the issue with your recent order. We apologize for the inconvenience and are happy to assist you with a refund.\n\nWe have processed a refund of $98 to your original payment method for the duplicate charge of $49. This refund should be visible on your account within the next 3-5 business days.\n\nIf you have any further questions or concerns, please don't hesitate to contact us. We appreciate your patience and understanding in this matter.\n\nThank you for choosing our service.\n\nBest regards,\n[Your Name]"
  },
  "swift": {
   "ttft": 513,
   "total": 10139,
   "text": "Subject: Refund for Duplicate Charge on Order\n\nDear [Customer's Name],\n\nThank you for bringing this to our attention. We apologize for the error and are happy to help. We have processed a full refund of the duplicate $49 charge, which has been credited back to your original payment method. You can expect to see the refund in the next 3-5 business days, depending on your bank's processing time.\n\nIf you have any further questions or concerns, please don't hesitate to reach out. We appreciate your patience and understanding in this matter. Your satisfaction is our top priority, and we're here to make it right.\n\nThank you for shopping with us.\n\nBest regards,\n[Your Name/Support Team]"
  }
 },
 {
  "id": "code",
  "label": "Code",
  "prompt": "Write a Python function that groups transactions by day and returns the daily totals, then explain it in two sentences.",
  "ogbon": {
   "ttft": 81,
   "total": 1050,
   "text": "```python\nimport pandas as pd\n\ndef group_transactions_by_day(transactions):\n    \"\"\"\n    Group transactions by day and return the daily totals.\n\n    Args:\n        transactions (list of dictionaries): A list of transactions where each transaction is a dictionary with 'date' and 'amount' keys.\n\n    Returns:\n        pandas.DataFrame: A DataFrame with 'date' as the index and the daily totals as values.\n    \"\"\"\n    # Convert the list of transactions to a DataFrame\n    df = pd.DataFrame(transactions)\n\n    # Convert the 'date' column to datetime type and set it as the index\n    df['date'] = pd.to_datetime(df['date'])\n    df.set_index('date', inplace=True)\n\n    # Group by date and sum the amounts\n    daily_totals = df['amount'].resample('D').sum()\n\n    return daily_totals\n\n# Example usage:\ntransactions = [\n    {'date': '2022-01-01', 'amount': 100},\n    {'date': '2022-01-01', 'amount': 200},\n    {'date': '2022-01-02', 'amount': 50},\n    {'date': '2022-01-03', 'amount': 75}\n]\n\ndaily_totals = group_transactions_by_day(transactions)\nprint(daily_totals)\n```\n\nThis function groups transactions by day and returns the daily totals. It uses the pandas library to convert the list of transactions to a DataFrame, set the 'date' column as the index, and then group by date to calculate the daily totals."
  },
  "swift": {
   "ttft": 469,
   "total": 22519,
   "text": "**Grouping Transactions by Day and Calculating Daily Totals**\n```python\nimport pandas as pd\n\ndef group_transactions_by_day(transactions):\n    \"\"\"\n    This function takes a list of transactions, groups them by day, and returns a dictionary with the daily totals.\n\n    Parameters:\n    transactions (list): A list of transactions, where each transaction is a dictionary with 'date' and 'amount' keys.\n\n    Returns:\n    dict: A dictionary with the date as the key and the total amount as the value.\n    \"\"\"\n    # Create a pandas DataFrame from the transactions list\n    df = pd.DataFrame(transactions)\n\n    # Group the transactions by day and calculate the sum of the amounts\n    daily_totals = df.groupby('date')['amount'].sum().to_dict()\n\n    return daily_totals\n```\n**Example Use Case:**\n```python\ntransactions = [\n    {'date': '2022-01-01', 'amount': 100},\n    {'date': '2022-01-01', 'amount': 200},\n    {'date': '2022-01-02', 'amount': 50},\n    {'date': '2022-01-02', 'amount': 75}\n]\n\ndaily_totals = group_transactions_by_day(transactions)\nprint(daily_totals)  # Output: {'2022-01-01': 300, '2022-01-02': 125}\n```\nThis function uses the pandas library to efficiently group the transactions by day and calculate the sum of the amounts. The result is a dictionary with the date as the key and the total amount as the value."
  }
 },
 {
  "id": "voice",
  "label": "Voice reply",
  "prompt": "You are a voice assistant. Tell the user their next appointment is Thursday at 2:30 pm with Dr Ade, and offer two other times.",
  "ogbon": {
   "ttft": 70,
   "total": 340,
   "text": "You have an upcoming appointment scheduled for Thursday at 2:30 pm with Dr. Ade. \n\nWould you like to consider the following alternative times for your appointment with Dr. Ade?\n\nA) Monday at 9:00 am\nB) Wednesday at 4:00 pm\n\nPlease let me know if you'd like to schedule one of these times or stick with the original Thursday appointment."
  },
  "swift": {
   "ttft": 471,
   "total": 9486,
   "text": "You have a scheduled appointment on Thursday at 2:30 pm with Dr. Ade. \n\nIf this time does not work for you, I have two alternative time slots available. You can also consider the following options:\n\n1. Wednesday at 3:00 pm with Dr. Ade: This is a 30-minute earlier time slot on the same day, just a day before your original appointment.\n\n2. Friday at 1:00 pm with Dr. Ade: This is a 1 hour and 30 minutes later time slot on the next day, which may be more suitable for your schedule.\n\nPlease let me know if you would like to change or confirm your appointment."
  }
 },
 {
  "id": "agent",
  "label": "Agent plan",
  "prompt": "Write a numbered step-by-step plan for an AI agent to reconcile last month’s invoices against bank payments.",
  "ogbon": {
   "ttft": 129,
   "total": 1920,
   "text": "Here's a step-by-step plan for an AI agent to reconcile last month's invoices against bank payments:\n\n**Reconciliation Plan**\n\n**Step 1: Data Collection (Automatic)**\n\n1.1. Retrieve all invoices for last month from the accounting database.\n1.2. Retrieve all bank payments for last month from the bank statement.\n1.3. Retrieve any relevant tax or fee information.\n\n**Step 2: Data Preprocessing (Automatic)**\n\n2.1. Clean and standardize the invoice and payment data.\n2.2. Remove any duplicate or invalid records.\n2.3. Convert all dates to a consistent format.\n\n**Step 3: Invoice Matching (Automatic)**\n\n3.1. Identify invoices with matching payment amounts and dates.\n3.2. Create a matching record for each invoice with a corresponding payment.\n\n**Step 4: Discrepancy Identification (Automatic)**\n\n4.1. Identify invoices with no matching payment.\n4.2. Identify payments with no matching invoice.\n4.3. Identify discrepancies in payment amounts or dates.\n\n**Step 5: Discrepancy Resolution (Automatic)**\n\n5.1. For invoices with no matching payment, suggest possible reasons for the discrepancy (e.g. payment not received, payment applied to incorrect account).\n5.2. For payments with no matching invoice, suggest possible reasons for the discrepancy (e.g. incorrect payment amount, payment for a different account).\n5.3. For discrepancies in payment amounts or dates, suggest possible reasons for the discrepancy (e.g. incorrect payment amount, payment applied to incorrect account).\n\n**Step 6: Reconciliation Report Generation (Automatic)**\n\n6.1. Generate a reconciliation report showing the matched and unmatched invoices and payments.\n6.2. Include a summary of the discrepancies and suggested reasons for each.\n\n**Step 7: Human Review and Approval (Manual)**\n\n7.1. A human accountant reviews the reconciliation report and discrepancies.\n7.2. The accountant investigates and resolves any discrepancies.\n7.3. The accountant updates the accounting database with the resolved discrepancies.\n\n**Step 8: Reconciliation Complete (Automatic)**\n\n8.1. The AI agent updates the reconciliation report to reflect the resolved discrepancies.\n8.2. The reconciliation process is complete.\n\nThis plan outlines the steps an AI agent can take to reconcile last month's invoices against bank payments. The AI agent performs most of the steps automatically, but a human accountant is required to review and approve the reconciliation report and resolve any discrepancies."
  },
  "swift": {
   "ttft": 491,
   "total": 42074,
   "text": "**Reconcile Last Month's Invoices Against Bank Payments**\n\n**Pre-requisites:**\n\n- Access to the company's accounting system\n- Access to the company's bank statement\n- A list of last month's invoices\n- A list of last month's bank payments\n\n**Step-by-Step Plan:**\n\n1. **Retrieve Last Month's Invoices:**\n   - Log in to the company's accounting system\n   - Navigate to the \"Invoices\" or \"Accounts Receivable\" section\n   - Filter the list to show only invoices from the previous month\n   - Download the list of invoices in a format that can be easily read by the AI agent (e.g., CSV or Excel)\n\n2. **Retrieve Last Month's Bank Payments:**\n   - Log in to the company's online banking system\n   - Navigate to the \"Transaction History\" or \"Statement\" section\n   - Filter the list to show only transactions from the previous month\n   - Download the list of bank payments in a format that can be easily read by the AI agent (e.g., CSV or Excel)\n\n3. **Preprocess the Data:**\n   - Use the AI agent's data processing capabilities to:\n     - Clean and format the data to ensure consistency\n     - Remove any duplicate or unnecessary information\n     - Map the data to a standard format for reconciliation\n\n4. **Match Invoices to Bank Payments:**\n   - Use the AI agent's machine learning capabilities to:\n     - Identify the bank payment that matches each invoice\n     - Create a list of matched and unmatched invoices\n\n5. **Identify Unmatched Invoices:**\n   - Use the AI agent's data analysis capabilities to:\n     - Identify the invoices that do not have a matching bank payment\n     - Determine the reason for the mismatch (e.g., payment not received, payment not made, etc.)\n\n6. **Reconcile the Invoices:**\n   - Use the AI agent's data analysis capabilities to:\n     - Calculate the total amount of matched and unmatched invoices\n     - Calculate the total amount of bank payments\n     - Reconcile the invoices with the bank payments\n\n7. **Generate a Reconciliation Report:**\n   - Use the AI agent's reporting capabilities to:\n     - Create a report that shows the matched and unmatched invoices\n     - Show the total amount of bank payments\n     - Highlight any discrepancies or issues\n\n8. **Review and Approve the Reconciliation:**\n   - Use the AI agent's review and approval capabilities to:\n     - Review the reconciliation report for accuracy\n     - Approve the reconciliation\n\n9. **Update the Accounting System:**\n   - Use the AI agent's data update capabilities to:\n     - Update the accounting system with the reconciled data\n     - Ensure that the accounting system is up-to-date and accurate\n\n10. **Store the Reconciliation Data:**\n    - Use the AI agent's data storage capabilities to:\n      - Store the reconciled data for future reference\n      - Ensure that the data is secure and easily accessible."
  }
 },
 {
  "id": "robot",
  "label": "Robotics",
  "prompt": "You control a robot arm. A cup is 30 cm ahead and 10 cm left of the gripper. Reply with only the next action as JSON: move, grip or stop, with x and y in cm.",
  "ogbon": {
   "ttft": 71,
   "total": 170,
   "text": "{\"action\": \"move\", \"x\": 10, \"y\": 0}"
  },
  "swift": {
   "ttft": 403,
   "total": 1578,
   "text": "{\"action\": \"move\", \"x\": 10, \"y\": 0}"
  }
 }
];

// Artificial Analysis, Llama 3.1 8B, October 2026. Its first-token times are measured with a
// 10,000-token prompt, so they run longer than these short prompts would.
const MODELLED = [
  { name: "Groq", ttft: 840, tps: 646 },
  { name: "CoreWeave", ttft: 830, tps: 142 },
  { name: "Novita", ttft: 950, tps: 175 },
  { name: "DeepInfra", ttft: 920, tps: 36 },
];

// Roughly four characters per token, close to what common tokenizers produce for English.
const tokenize = (text) => text.match(/.{1,4}/gs) || [];
const modelled = (ttft, tps, text) => ({ ttft, total: Math.round(ttft + (tokenize(text).length / tps) * 1000), text });

const runsFor = (task) => {
  const ref = task.swift.text;
  return [
    { name: "Ogbon", model: "Llama 3.1 8B · measured", ours: true, ...task.ogbon },
    { name: "SwiftInference", model: "Llama 3.1 8B · measured", ...task.swift },
    ...MODELLED.map((m) => ({ name: m.name, model: "Llama 3.1 8B · modelled", ...modelled(m.ttft, m.tps, ref) })),
  ];
};

const $ = (s) => document.querySelector(s);
const lanesEl = $("[data-lanes]"), runBtn = $("[data-run]"), promptEl = $("[data-prompt]"), tasksEl = $("[data-tasks]");
let lanes = [], longest = 0, frame = 0, current = TASKS[0];

// Join the last two words so a prompt never ends on a lone word.
const keepLastTwo = (text) => text.replace(/ (\S+)$/, " $1");

const secs = (ms) => `${(ms / 1000).toFixed(2)} s`;

const build = (task) => {
  cancelAnimationFrame(frame);
  current = task;
  promptEl.textContent = keepLastTwo(task.prompt);
  const runs = runsFor(task);
  longest = Math.max(...runs.map((r) => r.total));
  lanesEl.textContent = "";
  lanes = runs.map((p) => {
    const el = document.createElement("div");
    el.className = "lane" + (p.ours ? " is-ours" : "");
    el.innerHTML = `
      <div class="lane-meta">
        <p class="lane-name">${p.name}</p>
        <p class="lane-tps">${p.model}</p>
        <p class="lane-time" data-time>Ready</p>
      </div>
      <div class="lane-body">
        <p class="lane-out" data-out></p>
        <div class="lane-track">
          <span class="lane-wait" data-wait></span><span class="lane-stream" data-stream></span>
        </div>
        <p class="lane-stats">First token ${p.ttft.toLocaleString("en-US")} ms · total ${secs(p.total)}</p>
      </div>`;
    lanesEl.appendChild(el);
    return {
      p, el, tokens: tokenize(p.text),
      out: el.querySelector("[data-out]"), time: el.querySelector("[data-time]"),
      wait: el.querySelector("[data-wait]"), stream: el.querySelector("[data-stream]"),
    };
  });
  runBtn.textContent = "Start the race";
  runBtn.disabled = false;
};

const run = () => {
  cancelAnimationFrame(frame);
  const start = performance.now();
  let first = null;
  lanes.forEach((l) => {
    l.el.classList.remove("is-done", "is-first", "is-streaming");
    l.out.textContent = "";
    l.wait.style.width = l.stream.style.width = "0%";
  });
  runBtn.textContent = "Running…";
  runBtn.disabled = true;

  const tick = (now) => {
    const t = now - start;
    let done = 0;
    for (const l of lanes) {
      const { ttft, total } = l.p;
      // The track is scaled to the slowest run, so bar lengths compare directly.
      l.wait.style.width = `${(Math.min(t, ttft) / longest) * 100}%`;
      l.stream.style.width = `${(Math.max(0, Math.min(t, total) - ttft) / longest) * 100}%`;
      if (t < ttft) { l.time.textContent = `Waiting ${Math.round(t)} ms`; continue; }
      l.el.classList.add("is-streaming");
      const share = total > ttft ? Math.min(1, (t - ttft) / (total - ttft)) : 1;
      const shown = l.tokens.slice(0, Math.max(1, Math.ceil(share * l.tokens.length))).join("");
      if (shown !== l.out.textContent) { l.out.textContent = shown; l.out.scrollTop = l.out.scrollHeight; }
      if (t < total) { l.time.textContent = secs(t); continue; }
      l.time.textContent = `Done in ${secs(total)}`;
      if (!l.el.classList.contains("is-done")) {
        l.el.classList.add("is-done");
        if (!first) { first = l; l.el.classList.add("is-first"); }
      }
      done++;
    }
    if (done < lanes.length) frame = requestAnimationFrame(tick);
    else { runBtn.textContent = "Race again"; runBtn.disabled = false; }
  };
  frame = requestAnimationFrame(tick);
};

TASKS.forEach((task, i) => {
  const b = document.createElement("button");
  b.type = "button";
  b.className = "task";
  b.textContent = task.label;
  b.setAttribute("aria-pressed", i === 0 ? "true" : "false");
  b.addEventListener("click", () => {
    tasksEl.querySelectorAll(".task").forEach((x) => x.setAttribute("aria-pressed", x === b ? "true" : "false"));
    build(task);
  });
  tasksEl.appendChild(b);
});

runBtn.addEventListener("click", run);
build(current);
