/**
 * TaskList component - Displays jobs and LeetCode tasks
 */
'use client';

import React from 'react';
import { Task } from '@/services/api';
import { ExternalLink, Briefcase, Code } from 'lucide-react';

interface TaskListProps {
  tasks: Task[];
  onTaskClick?: (task: Task) => void;
  className?: string;
}

const TaskList: React.FC<TaskListProps> = ({ tasks, onTaskClick, className = '' }) => {
  const getTaskIcon = (type: string) => {
    switch (type) {
      case 'job':
        return <Briefcase className="w-5 h-5 text-blue-500" />;
      case 'leetcode':
        return <Code className="w-5 h-5 text-green-500" />;
      default:
        return <Briefcase className="w-5 h-5 text-gray-500" />;
    }
  };

  const getTaskTypeLabel = (type: string) => {
    switch (type) {
      case 'job':
        return 'Job Application';
      case 'leetcode':
        return 'LeetCode Problem';
      default:
        return 'Task';
    }
  };

  if (tasks.length === 0) {
    return (
      <div className={`text-center py-8 text-gray-500 ${className}`}>
        <p>No tasks for today. Generate tasks to get started!</p>
      </div>
    );
  }

  return (
    <div className={`space-y-3 ${className}`}>
      {tasks.map((task) => (
        <div
          key={task.id}
          className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow border border-gray-200 dark:border-gray-700"
        >
          <div className="flex items-start justify-between">
            <div className="flex items-start gap-3 flex-1">
              <div className="mt-1">
                {getTaskIcon(task.type)}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide">
                    {getTaskTypeLabel(task.type)}
                  </span>
                  {task.completed && (
                    <span className="text-xs bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200 px-2 py-0.5 rounded">
                      Completed
                    </span>
                  )}
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-1">
                  {task.title}
                </h3>
                {task.description && (
                  <p className="text-sm text-gray-600 dark:text-gray-300 line-clamp-2">
                    {task.description}
                  </p>
                )}
                <div className="mt-2 text-xs text-gray-500 dark:text-gray-400">
                  Created: {new Date(task.created_at).toLocaleDateString()}
                </div>
              </div>
            </div>
            {task.url && (
              <a
                href={task.url}
                target="_blank"
                rel="noopener noreferrer"
                className="ml-4 p-2 text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                onClick={(e) => {
                  e.stopPropagation();
                  if (onTaskClick) {
                    onTaskClick(task);
                  }
                }}
              >
                <ExternalLink className="w-5 h-5" />
              </a>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

export default TaskList;
