(defun which-line ()
  "Print the current buffer line number along with the total number of lines."
  (interactive)
  (let ((start (point-min))
        (n (line-number-at-pos)))
    (setq totalLines (count-lines (point-min) (point-max)))
    (if (= start 1)
	(message "Line %d of %d" n totalLines)
      (save-excursion
        (save-restriction
          (widen)
          (message "line %d (narrowed line %d)"
                   (+ n (line-number-at-pos start) -1) n))))))

  
