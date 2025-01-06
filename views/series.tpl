% rebase('base.tpl')

<nav><a href="/series_all/all">Toutes les séries</a> | <a href="/series_all/1">Séries finies</a> | <a href="/series_all/0">Séries en cours</a> | <a href="/series_all/2">Séries incomplètes</a></nav>
<br>
% for s in series:
     <p><a href="/series/{{ s.id }}">{{ s.title }}</a> |
     % if s.finished == 1:
          Série finie
     % elif s.finished == 0:
          Série en cours
     % elif s.finished == 2:
          Série incomplète
     % end
     </p>
% end
