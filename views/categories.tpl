% rebase('base.tpl')

% dif = ["A", "R", "BD", "C", "P"]
% for cat in categories:    
        % if cat.index not in dif and cat.index[2] == '0' and cat.index[1] == '0':
            <p class="n1" id="i_{{ cat.index }}">{{ cat.index }} | {{ cat.description }}</p>
        % elif cat.index not in dif and cat.index[2] == '0':
            <p class="n2" id="i_{{ cat.index }}">{{ cat.index }} | {{ cat.description }}</p>
        % else:
            <p class="n3" id="i_{{ cat.index }}">{{ cat.index }} | {{ cat.description }}</p>
        % end
% end

<script src="/static/js/dewey.js"></script>
