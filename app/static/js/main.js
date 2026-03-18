// ═══════════════════════════════════════════════════════════
// College Library Management System – Client-Side JavaScript
// ═══════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', function () {

    // ── Sidebar Toggle (Admin) ──
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function () {
            // On mobile, use show-mobile class
            if (window.innerWidth <= 768) {
                sidebar.classList.toggle('show-mobile');
            } else {
                sidebar.classList.toggle('collapsed');
            }
        });
    }

    // ── Client-Side Table Search / Filter ──
    initTableSearch('booksTable', 'tableSearchInput');
    initTableSearch('studentsTable', 'tableSearchInput');
    initTableSearch('transactionsTable', 'tableSearchInput');
    initTableSearch('historyTable', 'tableSearchInput');
    initTableSearch('recentTable', 'tableSearchInput');

    // Generic live-search for any table
    function initTableSearch(tableId, inputId) {
        // Also support the inline JS search boxes
        const table = document.getElementById(tableId);
        if (!table) return;

        // If there's no dedicated input, create a small one above the table
        let input = document.getElementById(inputId);
        if (!input) {
            // Check if we already added one
            if (table.parentElement.querySelector('.js-table-search')) return;

            const searchDiv = document.createElement('div');
            searchDiv.className = 'p-3 border-bottom js-table-search';
            searchDiv.innerHTML = `
                <div class="input-group input-group-sm">
                    <span class="input-group-text"><i class="bi bi-filter"></i></span>
                    <input type="text" class="form-control"
                           placeholder="Quick filter this table…" id="jsSearch_${tableId}">
                </div>
            `;
            table.parentElement.insertBefore(searchDiv, table);
            input = document.getElementById(`jsSearch_${tableId}`);
        }

        if (!input) return;

        input.addEventListener('keyup', function () {
            const filter = this.value.toLowerCase();
            const rows = table.querySelectorAll('tbody tr');
            rows.forEach(function (row) {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(filter) ? '' : 'none';
            });
        });
    }

    // ── Auto-dismiss alerts after 5 seconds ──
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });

    // ── Confirm delete modals (fallback for forms without onclick) ──
    document.querySelectorAll('.delete-form').forEach(function (form) {
        form.addEventListener('submit', function (e) {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
            }
        });
    });

});
