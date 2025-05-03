<div class="ranking-container">
    <div class="ranking-wrapper">
        <h1>Ranking</h1>
        <div class="ranking-list">
            <?php foreach ($topRanking as $index => $user): ?>
                <div class="ranking-entry">
                    <div class="ranking-position">#<?php echo $index + 1; ?></div>
                    <div class="ranking-info">
                        <div class="ranking-name"><?php echo htmlentities($user['name'], ENT_QUOTES | ENT_HTML5, 'UTF-8'); ?></div>
                        <div class="ranking-email"><?php echo htmlentities($user['email'], ENT_QUOTES | ENT_HTML5, 'UTF-8'); ?></div>
                    </div>
                    <div class="ranking-score"><?php echo htmlentities($user['score'], ENT_QUOTES | ENT_HTML5, 'UTF-8'); ?> pts</div>
                </div>
            <?php endforeach; ?>
        </div>

        <?php if ($userRanking): ?>
            <div class="ranking-user">
                <h2>Tu posición en el ranking</h2>
                <div class="ranking-entry highlight">
                    <div class="ranking-position">#<?php echo $userRanking['position']; ?></div>
                    <div class="ranking-info">
                        <div class="ranking-name"><?php echo htmlentities($userRanking['name'], ENT_QUOTES | ENT_HTML5, 'UTF-8'); ?></div>
                        <div class="ranking-email"><?php echo htmlentities($userRanking['email'], ENT_QUOTES | ENT_HTML5, 'UTF-8'); ?></div>
                    </div>
                    <div class="ranking-score"><?php echo htmlentities($userRanking['score'], ENT_QUOTES | ENT_HTML5, 'UTF-8'); ?> pts</div>
                </div>
            </div>
        <?php endif; ?>
    </div>
</div>